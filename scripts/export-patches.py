#!/usr/bin/env python3
"""Export only the explicitly reviewed customization paths from development checkouts."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("opencode", type=Path)
parser.add_argument("warp", type=Path)
args = parser.parse_args()
pins = json.loads((ROOT / "upstream.json").read_text())
paths = {
    "opencode": [
        "packages/opencode/src/server/routes/instance/httpapi/groups/session.ts",
        "packages/opencode/src/server/routes/instance/httpapi/handlers/session.ts",
        "packages/opencode/test/server/httpapi-session.test.ts",
        "packages/sdk/js/src/v2/gen/sdk.gen.ts",
        "packages/sdk/js/src/v2/gen/types.gen.ts",
        "packages/tui/src/app.tsx",
        "packages/tui/src/component/logo.tsx",
        "packages/tui/src/component/agent-timer.tsx",
        "packages/tui/src/component/dialog-content-width.tsx",
        "packages/tui/src/component/dialog-subagents.tsx",
        "packages/tui/src/component/dialog-usage.tsx",
        "packages/tui/src/config/keybind.ts",
        "packages/tui/src/context/content-width.ts",
        "packages/tui/src/context/sync.tsx",
        "packages/tui/src/context/theme.tsx",
        "packages/tui/src/context/thinking.ts",
        "packages/tui/src/logo.ts",
        "packages/tui/src/routes/home.tsx",
        "packages/tui/src/routes/session/index.tsx",
        "packages/tui/src/routes/session/sidebar.tsx",
        "packages/tui/src/theme/index.ts",
        "packages/tui/src/theme/assets/pivo-claude.json",
        "packages/tui/src/theme/assets/pivo-kimi.json",
        "packages/tui/src/util/agent-duration.ts",
        "packages/tui/src/util/important-tools.ts",
        "packages/tui/src/util/subscription-usage.ts",
        "packages/tui/src/util/presentation.ts",
        "packages/tui/test/app-lifecycle.test.tsx",
        "packages/tui/test/util/presentation.test.ts",
        "packages/tui/test/util/agent-duration.test.ts",
        "packages/tui/test/cli/tui/important-tools.test.ts",
        "packages/tui/test/cli/tui/subscription-usage.test.ts",
        "packages/tui/test/fixture/pivo-render-check.tsx",
        "packages/tui/test/fixture/pivo-demo.tsx",
        "packages/tui/test/pivo-thinking.test.tsx",
        "packages/tui/test/cli/cmd/tui/sync-live-hydration.test.tsx",
        "packages/tui/test/cli/cmd/tui/sync-undefined-messages.test.tsx",
    ],
    "warp": ["app/src/workspace/view/vertical_tabs.rs", "app/src/workspace/view/vertical_tabs_tests.rs"],
}
(ROOT / "patches").mkdir(exist_ok=True)
(ROOT / "licenses").mkdir(exist_ok=True)
for name, files in paths.items():
    source = getattr(args, name).resolve()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
    if head != pins[name]["commit"]:
        raise SystemExit(f"Wrong base for {name}: {head}")
    output = bytearray()
    for file in files:
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", file], cwd=source, capture_output=True).returncode == 0
        command = ["git", "diff", "--binary", "HEAD", "--", file] if tracked else ["git", "diff", "--binary", "--no-index", "--", "/dev/null", file]
        result = subprocess.run(command, cwd=source, capture_output=True)
        if result.returncode not in ([0] if tracked else [0, 1]):
            raise SystemExit(result.stderr.decode())
        output.extend(result.stdout)
    (ROOT / "patches" / f"{name}.patch").write_bytes(output)
    print(f"Exported {name}: {len(output)} bytes, {len(files)} reviewed paths")
shutil.copy2(args.opencode / "LICENSE", ROOT / "licenses/OPENCODE-MIT.txt")
shutil.copy2(args.warp / "LICENSE-AGPL", ROOT / "licenses/WARP-AGPL-3.0.txt")
shutil.copy2(args.warp / "LICENSE-MIT", ROOT / "licenses/WARP-MIT.txt")
for kind, pattern in [("warp", "*.yaml"), ("tui", "*.json")]:
    target = ROOT / "themes" / kind
    target.mkdir(parents=True, exist_ok=True)
    for file in (args.opencode / "themes" / kind).glob(pattern):
        shutil.copy2(file, target / file.name)
