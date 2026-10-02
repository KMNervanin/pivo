# Конфигурация, инструкции и навыки

Pivo использует окружение OpenCode, а не отдельный скрытый набор инструкций.
Репозиторий содержит код оболочки, все её custom commands и build-инструкции.
Личные промпты, рабочие политики, Obsidian vault, учётные данные и история владельца
не являются частью переносимого приложения и не публикуются.

- Глобальный config: `~/.config/opencode/opencode.json` / `.jsonc`.
- Project config: `opencode.json` / `.jsonc` или `.opencode/opencode.json`.
- Правила проекта: `AGENTS.md`; дополнительные файлы можно подключать через `instructions`.
- Agents: `.opencode/agents/*.md` или `~/.config/opencode/agents/*.md`.
- Skills: `.opencode/skills/<name>/SKILL.md`, `~/.config/opencode/skills/`, а также
  поддерживаемые upstream пути `~/.agents/skills/` и `~/.claude/skills/`.
- Custom commands: `.opencode/commands/*.md` или соответствующий глобальный каталог.
- TUI settings: `~/.config/opencode/tui.json`; пользовательские темы — `themes/` рядом.
- OAuth и база: штатные OpenCode data paths (на macOS обычно `~/.local/share/opencode`).

Объедини при необходимости `config-examples/opencode.json` со своим config. Он добавляет
пример read-only роли `reader`, manual share и отключение автообновления, не задаёт модель
или учётные данные. Не копируй пример поверх существующего файла целиком. После правки
config/agents/skills/plugins перезапусти Pivo — текущая сессия хранит загруженный config.

Дополнительные инструкции подключаются, например:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["docs/project-rules.md"],
  "skills": { "paths": ["./team-skills"] }
}
```

Локальный MCP задаётся объектом `mcp.<name>` с `type: "local"` и массивом `command`;
удалённый — `type: "remote"` и `url`. Токены передавай через `{env:VARIABLE}`, а не
литералы в репозитории. Permissions роли задаются явно; `reader` в примере запрещает
редактирование и shell. Набор серверов и доступы выбираются отдельно под твою среду.

Документация: [config](https://opencode.ai/docs/config/),
[MCP](https://opencode.ai/docs/mcp-servers/), [skills](https://opencode.ai/docs/skills/).
Она может описывать более новый upstream: для этой сборки схема и исходники закреплённого
checkout являются окончательной проверкой совместимости. Hooks другого harness сами по себе
в OpenCode не переносятся.
