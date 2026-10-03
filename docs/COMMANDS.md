# Все команды и пункты меню Pivo

Справочник для **1.18.34-pivo.7**, проверен по исходникам закреплённого OpenCode.
`/sidebar` и похожие «скиллы» интерфейса технически называются slash-командами:
они выполняют действие оболочки. Настоящие skills передают инструкции модели;
они описаны отдельно ниже. **Меню здесь — Command Palette Pivo (`Ctrl+P`), не настройки Warp.**

В таблицах «—» означает, что у пункта нет slash-команды: вызывай его из меню.
Названия переключателей меняются между Show/Hide и Enable/Disable по текущему состоянию.
Недоступные действия скрываются: список зависит от экрана, модели, настроек и plugins.
ID в последней колонке пригодится для поиска действия в keybindings/исходниках.

## Сессии и история

| Команда | Пункт меню | Что делает | ID |
| --- | --- | --- | --- |
| `/resume`, `/continue` | Switch session | Открывает список прежних сессий. Старое имя `/sessions` заменено. | `session.list` |
| `/new`, `/clear` | New session | Переходит к новому чату; старую историю не удаляет. | `session.new` |
| `/rename` | Rename session | Переименовывает текущую сессию. | `session.rename` |
| `/timeline` | Jump to message | Показывает сообщения для быстрого перехода по истории. | `session.timeline` |
| `/fork` | Fork session | Создаёт отдельную ветку разговора от выбранного сообщения. Это не Git branch. | `session.fork` |
| `/compact`, `/summarize` | Compact session | Просит модель сжать контекст текущей сессии; нужен подключённый provider. | `session.compact` |
| `/undo` | Undo previous message | Откатывает сессию к последнему пользовательскому запросу, возвращает его текст во ввод; работает через session revert и может откатить отслеживаемые изменения файлов. Активный ход прерывается. | `session.undo` |
| `/redo` | Redo | Возвращает следующий отменённый шаг; доступно после undo. | `session.redo` |
| `/share` | Share session / Copy share link | Публикует сессию через upstream share-сервис или копирует уже существующую ссылку. Недоступно при `share: disabled`. | `session.share` |
| `/unshare` | Unshare session | Отключает опубликованную ссылку текущей сессии. | `session.unshare` |
| `/copy` | Copy session transcript | Копирует текстовую расшифровку разговора в буфер. | `session.copy` |
| `/export` | Export session transcript | Сохраняет Markdown-файл; диалог позволяет выбрать имя, reasoning, инструменты, метаданные и открытие в редакторе. | `session.export` |
| — | Copy last assistant message | Копирует текст последнего ответа, а не всю сессию. | `messages.copy` |
| `/subagents` | View and launch subagents | Список дочерних задач, состояния, переход к истории/результату и запуск новой задачи через выбор роли. | `session.subagents` |
| `/steer` | Deliver queue after current step (keep running tasks) | Принимает сохранённую очередь для следующего шага, не отменяя tools и сабагентов. Черновик не отправляет; уже работающим детям уточнение автоматически не передаёт. | `session.steer` |

`/steer` доступен при наличии очереди у активного ответа. Обычный interrupt остаётся
отдельным действием и действительно прекращает текущую работу. Подробности очереди,
attachments и ограничений описаны в [USAGE](USAGE.md#очередь-и-steer).

## Модель, агенты и подключения

| Команда | Пункт меню | Что делает | ID |
| --- | --- | --- | --- |
| `/models`, `/mo` | Switch model | Выбор доступной модели и управление избранными в диалоге. | `model.list` |
| `/variants` | Switch model variant | Выбор варианта модели, например уровня reasoning; появляется, только если у модели есть варианты. | `variant.list` |
| — | Variant cycle | Переключает следующий вариант текущей модели. | `variant.cycle` |
| `/agents` | Switch agent | Выбирает основного агента/режим работы. Не путать с меню дочерних задач `/subagents`. | `agent.list` |
| `/connect` | Connect provider | Подключение поставщика моделей: выбор провайдера и предусмотренного им способа входа. | `provider.connect` |
| `/org`, `/orgs`, `/switch-org` | Switch org | Переключение организации OpenCode Console; только при нескольких доступных организациях. | `console.org.switch` |
| `/mcps` | Toggle MCPs | Список MCP-серверов, их состояние и переключение подключения. | `mcp.list` |
| `/status` | View status | Диагностика текущего окружения и подключений. | `opencode.status` |
| `/usage` | View subscription usage | Остатки квоты OpenAI OAuth и время сброса окон. Не вызывает модель; не показывает универсальную квоту всех провайдеров. | `pivo.usage` |
| — | Enable / Disable auto-approve permissions | Переключает автоматические ответы на запросы разрешений. Это настройка выполнения, а не оформления. | `permission.mode` |

## Вид чата и sidebar

| Команда | Пункт меню | Что делает | ID |
| --- | --- | --- | --- |
| `/sidebar` | Show / Hide sidebar | Переключает правую панель с таймером, контекстом и MCP. На широком экране панель занимает отдельную колонку, на узком открывается поверх чата. | `session.sidebar.toggle` |
| `/width` | Adjust chat width | Ползунок ширины чата и ввода 40–100%; окно терминала не меняется, sidebar учитывается отдельно. | `pivo.width` |
| `/thinking`, `/toggle-thinking` | Show / Hide thinking | Показывает или полностью скрывает reasoning-блоки. На работу модели и сохранённую историю не влияет. | `session.toggle.thinking` |
| `/tools` | Show / Hide tool details | Переключает видимость инструментов; ошибки и текущая работа не должны теряться. | `session.toggle.actions` |
| `/important` | Show all tools / Show only important tools | Переключает полный и компактный отфильтрованный список инструментов. | `session.toggle.important` |
| `/timestamps`, `/toggle-timestamps` | Show / Hide timestamps | Показывает время сообщений. | `session.toggle.timestamps` |
| — | Enable / Disable code concealment | Управляет сокрытием разметки в отображении кода/Markdown; исходное содержимое сохраняется. | `session.toggle.conceal` |
| — | Toggle session scrollbar | Показывает или скрывает scrollbar истории. | `session.toggle.scrollbar` |
| — | Show / Hide generic tool output | Показывает или скрывает полный вывод generic tools. | `session.toggle.generic_tool_output` |
| — | Enable / Disable diff wrapping | Переносит длинные строки diff либо оставляет их без переноса. | `app.toggle.diffwrap` |
| — | Enable / Disable file context | Включает/выключает файловый контекст из выделения подключённого редактора для текущего ввода. | `app.toggle.file_context` |
| — | Enable / Disable paste summary | Сворачивает большие вставки во вводе до краткой подписи; полный текст сохраняется в parts. | `app.toggle.paste_summary` |
| — | Enable / Disable session directory filtering | Ограничивает список сессий текущей директорией либо показывает более широкий список проекта. | `app.toggle.session_directory_filter` |

`/sidebar` работает внутри сессии. В дочернем чате upstream не рендерит sidebar;
на стартовом экране нет контекста сессии и этой команды. Скрытие сохраняется, а
режим Show возвращает штатное `auto`: при новом открытии узкого окна панель сама
не раскрывается, но её можно вызвать вручную. Широким считается терминал более 120 колонок.

## Ввод, черновики и рабочее пространство

| Команда | Пункт меню | Что делает | ID |
| --- | --- | --- | --- |
| `/editor` | Open editor | Открывает текущий черновик во внешнем редакторе и возвращает отредактированный текст во ввод. | `prompt.editor` |
| — | Remove editor context | Убирает контекст, присланный интеграцией редактора; доступно при его наличии. | `prompt.editor_context.clear` |
| — | Stash prompt | Откладывает текущий черновик с его parts и освобождает поле ввода. | `prompt.stash` |
| — | Stash pop | Возвращает последний отложенный черновик. | `prompt.stash.pop` |
| — | Stash list | Открывает список отложенных черновиков для выбора. | `prompt.stash.list` |
| `/skills` | Skills | Показывает обнаруженные навыки с описаниями; выбор подставляет `/<имя> ` во ввод. Само открытие списка не запускает навык. | `prompt.skills` |
| `/move` | Move session | Переносит сессию в другую директорию проекта через диалог. | `session.move` |
| `/workspaces` | Manage workspaces | Управление workspaces; экспериментальная возможность, скрыта без `OPENCODE_EXPERIMENTAL_WORKSPACES`. | `workspace.list` |
| `/warp` | Warp | Меняет workspace текущей сессии, если включены experimental workspaces. **Это не приложение Warp Terminal.** | `workspace.set` |
| — | Copy worktree path | Копирует путь активного worktree workspace; только когда такой workspace выбран. | `workspace.copy_path` |

## Темы, plugins и системные действия

| Команда | Пункт меню | Что делает | ID |
| --- | --- | --- | --- |
| `/themes` | Switch theme | Открывает список тем, включая `pivo-kimi`, Claude-палитры и установленные custom themes. Пользовательский текст в Pivo-палитрах жирный. | `theme.switch` |
| — | Switch to light / dark mode | Переключает светлый/тёмный вариант темы. | `theme.switch_mode` |
| — | Lock / Unlock theme mode | Закрепляет режим темы либо возвращает автоматическое определение. | `theme.mode.lock` |
| — | Enable / Disable animations | Включает или выключает анимации интерфейса. | `app.toggle.animations` |
| — | Enable / Disable terminal title | Разрешает Pivo менять заголовок вкладки терминала. | `terminal.title.toggle` |
| — | Show / Hide tips | Подсказки на стартовом экране; пункт предоставляется встроенным home-tips plugin. | `tips.toggle` |
| — | Plugins | Список TUI plugins, их состояние и переключение. | `plugins.list` |
| — | Install plugin | Диалог установки TUI plugin. | `plugins.install` |
| `/help` | Help | Справка по управлению и горячим клавишам. | `help.show` |
| — | Open docs | Открывает сайт документации OpenCode во внешнем браузере. | `docs.open` |
| `/debug` | View debug info | Показывает диагностическую информацию приложения. | `opencode.debug` |
| — | Toggle debug panel | Переключает отладочную панель renderer. | `app.debug` |
| — | Toggle console | Переключает встроенную диагностическую консоль. | `app.console` |
| — | Write heap snapshot | Записывает снимок памяти для диагностики; путь показывается в уведомлении. | `app.heap_snapshot` |
| `/exit`, `/quit`, `/q` | Exit the app | Выходит из оболочки; для продолжения используй `pivo --continue`. | `app.exit` |

## Diff viewer

`/diff` — пункт **Open diff viewer** (`diff.open`), встроенный plugin просмотра изменений.
Внутри выбирается источник: **Working tree**, **Main branch** (если доступна), **Last turn**.
Это просмотр diff, а не команда commit/push. Действия ниже относятся к экрану viewer,
а не являются самостоятельными `/...` командами в чате:

| Действие | Что делает | ID |
| --- | --- | --- |
| Close diff viewer | Возвращается к предыдущему экрану. | `diff.close` |
| Move diff viewer down / up | Движение вниз/вверх. | `diff.down`, `diff.up` |
| Page diff viewer down / up | Прокрутка страницами. | `diff.page.down`, `diff.page.up` |
| Toggle diff viewer item | Раскрывает/сворачивает выбранный элемент дерева. | `diff.toggle` |
| Expand diff viewer item | Раскрывает выбранный элемент. | `diff.expand` |
| Expand all diff viewer folders | Раскрывает все папки дерева. | `diff.expand_all` |
| Collapse diff viewer item | Сворачивает элемент дерева. | `diff.collapse` |
| Jump to next / previous diff hunk | Переход между блоками изменений. | `diff.next_hunk`, `diff.previous_hunk` |
| Jump to next / previous diff file | Переход между файлами. | `diff.next_file`, `diff.previous_file` |
| Toggle selected diff file reviewed | Помечает файл просмотренным/непросмотренным. | `diff.mark_reviewed` |
| Switch diff viewer focus | Переключает фокус дерева/содержимого. | `diff.switch_focus` |
| Toggle diff viewer file tree | Показывает/скрывает дерево файлов. | `diff.toggle_file_tree` |
| Toggle single patch view | Переключает просмотр одного patch. | `diff.single_patch` |
| Switch diff viewer source | Выбирает источник diff. | `diff.switch_source` |
| Toggle diff viewer split or unified view | Меняет side-by-side и unified представления. | `diff.toggle_view` |
| Show more diff viewer shortcuts | Показывает дополнительные сочетания клавиш viewer. | `diff.help` |

## Команды, которые запускают модель, и настоящие skills

В поставке upstream есть две command templates:

| Команда | Назначение |
| --- | --- |
| `/init` | Исследует проект и помогает создать/обновить `AGENTS.md` с правилами работы. |
| `/review [commit\|branch\|pr]` | Запускает ревью выбранных изменений; без аргумента — незакоммиченных. По умолчанию выполняется как subtask. |

Встроенный навык **`/customize-opencode`** объясняет и помогает настраивать OpenCode:
config, agents, skills, custom commands, plugins, MCP и permissions. В отличие от
`/sidebar`, его содержимое получает агент и затем выполняет задачу; это не мгновенное
действие UI.

Остальные настоящие навыки приходят из твоего окружения и проекта: например,
`.opencode/skills/<name>/SKILL.md`, `~/.config/opencode/skills/`, `~/.agents/skills/`
и дополнительных `skills.paths`. Полный **актуальный для запущенной сессии** перечень
с описаниями открывается через `/skills`. Сторонние MCP также могут добавлять prompts,
а config — свои команды. Они не являются фиксированной частью Pivo, поэтому их нельзя
объявлять встроенными или обещать одинаковый список у всех установок.

Для просмотра назначения навыка выбери его в `/skills`; для вызова используй
`/<имя-навыка> <задача>`. Skills, подключённые только в личной конфигурации разработчика,
не входят в этот публичный build-репозиторий. Схема установки описана в
[CONFIGURATION](CONFIGURATION.md).

## Управление клавиатурой и подсказки

Некоторые зарегистрированные действия намеренно скрыты из обычного меню и работают
через keybindings. Точные сочетания зависят от `tui.json`; посмотреть их можно в `/help`
и в панели which-key. Среди них:

- `prompt.submit`, `prompt.clear`, `prompt.paste` — отправить, очистить, вставить.
- `prompt.history.previous`, `prompt.history.next` — предыдущий/следующий ввод.
- `session.interrupt` — остановить текущий ход (штатная защита двойным нажатием).
- `session.page.up/down`, `session.line.up/down`, `session.half.page.up/down`,
  `session.first`, `session.last`, `session.messages_last_user`, `session.message.next/previous`
  — прокрутка и переходы по истории.
- `session.quick_switch.1` … `session.quick_switch.9` — быстрые слоты сессий.
- `model.cycle_recent`, `model.cycle_recent_reverse`, `model.cycle_favorite`,
  `model.cycle_favorite_reverse` — переключение недавних/избранных моделей.
- `agent.cycle`, `agent.cycle.reverse` — следующий/предыдущий основной агент.
- `session.child.first`, `session.parent`, `session.child.next`, `session.child.previous`
  — переходы между родительской и дочерними сессиями.
- `session.background` — перевод поддерживаемых foreground subagents в background.
- `terminal.suspend` — приостановить TUI-процесс (не Windows).

Which-key предоставляет **Show key bindings**, **Toggle key bindings layout**
(dock/overlay) и **Toggle pending key preview** (подсказка незаконченной последовательности).
Это действия plugin, не отдельные slash-команды. Его панель поддерживает смену групп,
прокрутку строками/страницами и переход к первой/последней привязке.

Источники проверки: `packages/tui/src/app.tsx`, `routes/session/index.tsx`,
`component/prompt/index.tsx`, `feature-plugins/`, а также
`packages/opencode/src/command/index.ts` в подготовленном checkout. Plugins и custom
commands могут расширять меню после запуска; **Suggested** — быстрые ссылки на те же
действия, а не дополнительный набор команд.
