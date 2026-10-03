# Проверки Pivo

## 1.18.34-pivo.7 — 03.10.2026

- Причина недоступного начала истории: upstream загружал `limit: 100`, обрезал
  hydrated список до 100 и удалял самое старое сообщение при каждом новом live event.
  Reproducer дал **RED 2/2**: в обоих сценариях получено 100 вместо 165 сообщений.
- Исправление сохраняет всю историю, включая parts, при hydration и streaming.
  Проверены stale hydration/live delta и concurrent removal; удалённые сообщения
  не восстанавливаются из старого ответа. HTTP failure остаётся non-crashing и допускает retry.
- Native render-fixture начинает с 120 ранних сообщений, добавляет 120 ответов и
  снова показывает первый текст через `session.first`. Установленный `.7` также
  открыл длинную пользовательскую сессию в отдельном tmux: после `Ctrl+G` исходное
  первое сообщение снова видно. Новых запросов к модели не отправлялось.
- Новый `pivo-kimi` использует точные основные цвета Kimi Code 2.1.1, собственные
  фоновые панели Pivo и существующий шрифт терминала. Renderer проверяет bold у
  пользователя в Kimi/Claude, отсутствие этого override в обычной upstream-теме.
- TUI suite: **212 pass, 1 skip, 0 fail**, 8 snapshots; typecheck проходит.
- Семь демонстрационных PNG захвачены из native OpenTUI spans и rasterized шрифтом Hack.
  Sidebar, compact/full/hidden tools, width slider и subagents используют production
  компоненты. Все provider/MCP/message данные синтетические; никакой личной истории.

## 1.18.34-pivo.6 — 03.10.2026

- `/sidebar` зарегистрирован на существующем `session.sidebar.toggle`, без изменения
  механики layout или отдельного model skill.
- Render-fixture вводит именно `/sidebar` через поле ввода: hide/show на 160 колонках
  и hide/show/hide на 100 колонках. Проверяется видимость sidebar и границы ввода;
  команда не создаёт дополнительного запроса к модели.
- TUI typecheck и suite: **209 pass, 1 skip, 0 fail**, 8 snapshots.
- `docs/COMMANDS.md` содержит все 86 обнаруженных non-hidden command registrations
  проверенных app/session/prompt/plugin/viewer модулей; пропущенных ID при AST-сверке нет.
  Это число включает контекстные действия diff viewer, а не 86 одновременных пунктов `Ctrl+P`.
  В справочнике отдельно указаны aliases, условные команды, hidden keyboard actions,
  `/init`, `/review`, встроенный skill и расширяемый список пользовательских skills.

## 1.18.34-pivo.5

macOS arm64, 2026-10-02/03. Все числа ниже относятся к этому кандидату.

## Pivo

- Чистый checkout upstream по `upstream.json`, применение опубликованного патча через
  `scripts/build.py`, установка frozen dependencies и сборка native binary прошли.
- Smoke: бинарник возвращает `1.18.34-pivo.5`; установка launcher и executable проверена.
- TUI typecheck проходит; suite: **209 pass, 1 skip, 0 fail**, 8 snapshots.
- HTTP session suite: **23 pass, 0 fail**. Типизация server package также проверена.
- В render-fixture настоящий sidebar показывает таймер, значение растёт во время busy,
  после completion остаётся `1:02`; проверены длинная история, ввод и размеры терминала.
- Проверены tool-round/retry timestamps, queued input, новый запрос, resume, abort,
  неполная idle-история и длительности больше суток.
- Регрессия `/steer` доказана RED/GREEN: прежняя реализация давала `task.state=error`
  вместо `running`. Исправленная сохраняет работающего сабагента, получает его результат
  вместе с двумя queued messages и вложением, не дублирует сообщение при двойном клике.
- Generated SDK обновлён генератором; generation нового client package не создала diff.

В upstream TUI-suite есть диагностический вывод негативного bootstrap-теста и отсутствующего
временного `kv.json`; итог тестов зелёный. Targeted lint новых timer/fixture файлов чист;
в server-файлах остаются существующие type-assertion warnings и warning `toSorted` в тесте.

## Warp

- `cargo build --locked --bin warp-oss --features gui` проходит.
- Targeted Clippy `-D warnings` проходит; изменённые файлы обработаны rustfmt.
- Тест production helper подписи: папка+ветка, папка без Git, `/`, ветка без папки,
  пустые значения. Запущены извлечённые **дословно** функция и её repository test через
  `rustc --test`; полный Warp test suite не запускался.
- Чистый upstream checkout принял Warp patch и LFS; оба изменённых файла побайтово
  совпали с файлами, из которых собрана `.app`.
- Упаковка `.app`, генерация third-party notices, AGPL/MIT notices и ad-hoc подпись
  проверены, `codesign --verify --deep --strict` проходит.
- Большая кружка видна на пользовательском скриншоте; возвращение нижней панели
  пользователь подтвердил. Новая комбинированная подпись требует перезапуска установленного
  Warp Pivo; pixel-аудит именно этой подписи в живом пользовательском окне не проводился.

Рабочие вкладки пользователя не перезапускались. Свежая `.app` установлена рядом с резервной
копией прежней; новые возможности кода Warp вступают в силу при следующем запуске приложения.
Проверки на Intel Mac, Linux и Windows не проводились. Бинарные релизы не публикуются.
