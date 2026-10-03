# Демонстрационные кадры

Все семь PNG захватывают настоящий layout, цвета и атрибуты native OpenTUI renderer:
чат в `pivo-kimi` и `pivo-claude`, `/width`, `/subagents`, полный/компактный/скрытый
режим инструментов на одной и той же переписке. Используются отдельное
временное состояние и локальные fixtures; ни OAuth, ни MCP сети, ни вызовов модели нет.
Данные, результаты инструментов, provider и квота в кадре синтетические.

PNG создаётся из цветных terminal-cell spans, а не путём фотографирования рабочего
стола. Pillow наносит текст шрифтом Hack Regular/Bold. Числа контекста/таймера взяты
из fixture; это демонстрация интерфейса, не отчёт о реальном API-расследовании.
Кадр не включает рамку Warp: он подходит для Pivo в любом терминале.

## Повторение

Сначала `python3 scripts/build.py prepare opencode` и frozen install зависимостей
в `.build/opencode`. Затем из корня build-репозитория:

```sh
mkdir -p .build/captures
PIVO_DEMO_OUTPUT="$PWD/.build/captures" OPENCODE_VERSION=1.18.34-pivo.7 \
  bun run --cwd .build/opencode/packages/tui test/fixture/pivo-demo.tsx
uv run --with pillow==12.0.0 python scripts/render-captures.py \
  .build/captures docs/screenshots --font /absolute/path/Hack-Regular.ttf
```

Hack можно взять из подготовленного Warp checkout:
`.build/warp/app/assets/bundled/fonts/hack/Hack-Regular.ttf`. Его лицензия MIT
лежит рядом в `LICENSE.md`. Шрифтовые файлы в этом репозитории не распространяются.
Можно указать другой моноширинный font; если соседний Bold-файл найден, скрипт
использует его для атрибута bold. Так оформление остаётся тем же, а метрики текста
будут соответствовать выбранному шрифту.
