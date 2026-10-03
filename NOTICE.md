# Licensing and upstream sources

Pivo is an independent customization; it is not an official OpenCode or Warp release.
OpenCode and Warp names and trademarks belong to their respective owners.

- Build scripts and original documentation: MIT, see `LICENSE`.
- `patches/opencode.patch`, OpenCode-derived themes and launcher: MIT, including
  copyright (c) 2025 opencode. See `licenses/OPENCODE-MIT.txt`.
- `patches/warp.patch`: AGPL-3.0-only, like the Warp application. The MIT license
  at repository root does **not** relicense this patch or the Warp application.
  See `licenses/WARP-AGPL-3.0.txt` and `licenses/WARP-MIT.txt` (WarpUI only).
- Dependency and bundled font licenses remain applicable. Warp's bundle builder
  generates `THIRD_PARTY_LICENSES.txt`; license-generation failure fails the build.
- `pivo-kimi` adapts palette values from Kimi Code 2.1.1, copyright (c) 2026 Moonshot AI,
  MIT. See `licenses/KIMI-MIT.txt` and https://github.com/MoonshotAI/kimi-code.
  Background surfaces are Pivo-specific; no Kimi application code or fonts are bundled.

Modified on 2026-10-02: OpenCode TUI branding, reasoning/tool presentation, themes,
quota dialog, queued steering, subagent menu, content width and agent timer;
Warp vertical-tab icon for Pivo, its line-height correction, and combined working-directory/Git-branch subtitles.

Exact upstream repositories and revisions are in `upstream.json`. The prepare
script fetches those revisions and applies the complete patches, including new
files and tests. Generated upstream checkouts retain their original license and
attribution files. No proprietary Warp server, Drive backend or Oz code is included.
Running the independent Pivo CLI inside Warp does not combine their source licenses.

This repository publishes **source patches and build recipes**, not binary releases.
Before redistributing a Warp binary, provide the complete corresponding source for
that precise build (including this recipe and required source dependencies), retain
the notices, and meet AGPL sections 5/6 and, where applicable, 13. A link to a mutable
upstream branch is not a substitute for preserving the corresponding version. For
Pivo binaries retain MIT/dependency notices as well. Local ad-hoc signing is not
Apple notarization.

Source recipe: https://github.com/KMNervanin/pivo
Upstream: https://github.com/anomalyco/opencode and https://github.com/warpdotdev/warp
