#!/usr/bin/env python3
"""Build pinned Pivo sources without importing the developer's home configuration."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "upstream.json").read_text())


def run(*args, cwd=ROOT, env=None):
    print("+", " ".join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True)


def prepare(name):
    source = ROOT / ".build" / name
    pin = LOCK[name]
    patch = ROOT / "patches" / f"{name}.patch"
    fingerprint = hashlib.sha256(patch.read_bytes()).hexdigest()
    marker = source / ".git" / "pivo-patch.json"
    expected = {"commit": pin["commit"], "patch": fingerprint}
    if source.exists():
        if marker.exists() and json.loads(marker.read_text()) == expected:
            return source
        raise SystemExit(f"Existing checkout differs or preparation was interrupted: {source}. Move it aside before retrying.")
    source.mkdir(parents=True)
    env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
    run("git", "init", source)
    run("git", "remote", "add", "origin", pin["url"], cwd=source)
    run("git", "fetch", "--depth=1", "origin", pin["commit"], cwd=source, env=env)
    run("git", "checkout", "--detach", "FETCH_HEAD", cwd=source, env=env)
    run("git", "apply", "--check", patch, cwd=source)
    run("git", "apply", patch, cwd=source)
    if name == "warp":
        run("git", "lfs", "pull", cwd=source)
    marker.write_text(json.dumps(expected) + "\n")
    return source


def bun(*args, source):
    run("bun", *args, cwd=source)


def build_pivo(source):
    version = subprocess.check_output(["bun", "--version"], text=True).strip()
    if version != "1.3.14":
        raise SystemExit(f"Bun 1.3.14 required, found {version}")
    bun("install", "--frozen-lockfile", source=source)
    env = dict(os.environ, OPENCODE_VERSION=LOCK["version"], OPENCODE_CHANNEL="latest")
    run("bun", "run", "packages/opencode/script/build.ts", "--single", "--skip-install", "--skip-embed-web-ui", cwd=source, env=env)
    osname = {"Darwin": "darwin", "Linux": "linux"}[platform.system()]
    arch = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x64"}[platform.machine()]
    binary = source / f"packages/opencode/dist/opencode-{osname}-{arch}/bin/opencode"
    output = ROOT / "dist" / "pivo"
    output.parent.mkdir(exist_ok=True)
    shutil.copy2(binary, output)
    print(f"Built {output}")


def build_warp(source):
    if platform.system() != "Darwin":
        raise SystemExit("This Warp bundle script supports macOS. See upstream for Linux/Windows.")
    env = dict(os.environ, CARGO_PROFILE_DEV_DEBUG="0", CARGO_INCREMENTAL="0")
    env.setdefault("CARGO_TARGET_DIR", str(ROOT / ".build" / "warp-target"))
    run("cargo", "build", "--locked", "--bin", "warp-oss", "--features", "gui", cwd=source, env=env)
    run("cargo", "bundle", "--bin", "warp-oss", "--features", "gui", cwd=source / "app", env=dict(env, CARGO_BUNDLE_SKIP_BUILD="1"))
    bundle = Path(env["CARGO_TARGET_DIR"]) / "debug/bundle/osx/WarpOss.app"
    run(source / "script/macos/add_framework_rpath", bundle / "Contents/MacOS/warp-oss", cwd=source)
    env.update(WARP_SCHEME_NAME="warposs", WARP_PLIST_PATH=str(bundle / "Contents/Info.plist"))
    run(source / "script/update_plist", cwd=source, env=env)
    # Upstream's dev runner skips notices; keep them in this distributable bundle.
    env.pop("NO_LICENSES", None)
    env["SKIP_SETTINGS_SCHEMA"] = "1"
    run(source / "script/prepare_bundled_resources", bundle / "Contents/Resources", "oss", cwd=source, env=env)
    for license_name in ["LICENSE-AGPL", "LICENSE-MIT"]:
        shutil.copy2(source / license_name, bundle / "Contents/Resources" / license_name)
    shutil.copy2(ROOT / "NOTICE.md", bundle / "Contents/Resources/PIVO-NOTICE.md")
    for key in ["CFBundleName", "CFBundleDisplayName"]:
        run("/usr/libexec/PlistBuddy", "-c", f"Set :{key} Warp Pivo", bundle / "Contents/Info.plist")
    run("codesign", "--force", "--deep", "--options", "runtime", "--sign", "-", bundle, "--entitlements", source / "script/Debug-Entitlements.plist")
    run("codesign", "--verify", "--deep", "--strict", bundle)
    output = ROOT / "dist" / "Warp Pivo.app"
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(bundle, output, symlinks=True)
    print(f"Built {output}. No running application was restarted.")


def install_pivo():
    home = Path.home()
    target = home / ".local/share/pivo"
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "dist/pivo", target / "opencode.new")
    os.replace(target / "opencode.new", target / "opencode")
    launcher = home / ".local/bin/pivo"
    launcher.parent.mkdir(parents=True, exist_ok=True)
    staging = launcher.with_name("pivo.new")
    shutil.copy2(ROOT / "scripts/pivo", staging)
    staging.chmod(0o755)
    os.replace(staging, launcher)
    print(f"Installed {launcher}. Add ~/.local/bin to PATH. Existing sessions keep their executable.")


def install_warp():
    source = ROOT / "dist/Warp Pivo.app"
    target = Path("/Applications/Warp Pivo.app")
    staging = target.with_name(f".Warp Pivo-{time.time_ns()}.app")
    shutil.copytree(source, staging, symlinks=True)
    run("codesign", "--verify", "--deep", "--strict", staging)
    if target.exists():
        backup = target.with_name(f"Warp Pivo-backup-{time.time_ns()}.app")
        target.rename(backup)
        print(f"Previous app kept at {backup}")
        try:
            staging.rename(target)
        except OSError:
            backup.rename(target)
            raise
    else:
        staging.rename(target)
    print(f"Installed {target}. Quit/reopen Warp Pivo when your running sessions are ready; no process was stopped.")


def install_themes():
    for directory in [Path.home() / ".warp/themes", Path.home() / ".warp-oss/themes"]:
        directory.mkdir(parents=True, exist_ok=True)
        for file in (ROOT / "themes/warp").glob("*.yaml"):
            shutil.copy2(file, directory / file.name)
    directory = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "opencode/themes"
    directory.mkdir(parents=True, exist_ok=True)
    for file in (ROOT / "themes/tui").glob("*.json"):
        shutil.copy2(file, directory / file.name)
    print("Themes installed; active theme unchanged.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "build", "test", "install-pivo", "install-warp", "install-themes"])
    parser.add_argument("component", choices=["opencode", "warp"], nargs="?", default="opencode")
    parser.add_argument("--source", type=Path, help="Use an existing patched development checkout")
    args = parser.parse_args()
    if args.action == "install-pivo":
        return install_pivo()
    if args.action == "install-warp":
        return install_warp()
    if args.action == "install-themes":
        return install_themes()
    source = args.source.resolve() if args.source else prepare(args.component)
    if args.action == "prepare":
        print(source)
        return
    if args.action == "test":
        if args.component == "opencode":
            bun("install", "--frozen-lockfile", source=source)
            bun("typecheck", source=source / "packages/tui")
            bun("test", source=source / "packages/tui")
            bun("test", "test/server/httpapi-session.test.ts", "--timeout", "30000", source=source / "packages/opencode")
            return
        run("cargo", "clippy", "--locked", "-p", "warp", "--bin", "warp-oss", "--features", "gui", "--no-deps", "--", "-D", "warnings", cwd=source)
        return
    if args.component == "opencode":
        return build_pivo(source)
    build_warp(source)


if __name__ == "__main__":
    main()
