import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Side, Todo, ToolMode } from '../types'

const PANE = 'pivo-sidebar'

const side = atom({ plugin: 'pivo', key: 'side' } as const, { isOpen: false } as Side)
const todos = atom({ plugin: 'pivo', key: 'todos' } as const, [] as Todo[])
const tick = atom({ plugin: 'pivo', key: 'tick' } as const, 0)
const tools = atom({ plugin: 'pivo', key: 'tools' } as const, 'all' as ToolMode)
const accent = atom({ plugin: 'pivo', key: 'accent' } as const, false)

// Routine calls: reads, searches, listings, bookkeeping. Everything else (edits, shell,
// questions, agents, MCP) is important; an errored call is always shown.
const ROUTINE = new Set(['Read', 'Grep', 'Glob', 'LS', 'ToolSearch', 'TodoWrite', 'ListMcpResourcesTool', 'ReadMcpResourceTool', 'ReadMcpResourceDirTool', 'Monitor', 'WebSearch', 'WebFetch'])
const MODES: ToolMode[] = ['all', 'important', 'none']

function isHidden(mode: ToolMode, tool: string, isErrored: boolean): boolean {
  if (mode === 'all' || isErrored) return false
  if (mode === 'none') return true
  return ROUTINE.has(tool)
}

async function openSidebar($: EngineInterface): Promise<void> {
  await $.ui.open({ id: PANE, title: 'Pivo', columns: 36 })
  await update($, side, () => ({ isOpen: true }))
  await $.store.set('sidebar', true)
}

// Global MCP servers live in ~/.claude.json, project ones in settings; names only,
// the engine does not expose their connection state to plugins.
async function mcpServers($: EngineInterface): Promise<string[]> {
  const names = new Set<string>()
  try {
    const home = (await $.env.get('HOME')) ?? ''
    const cfg = JSON.parse(await $.fs.read(`${home}/.claude.json`)) as { mcpServers?: Record<string, unknown> }
    for (const n of Object.keys(cfg.mcpServers ?? {})) names.add(n)
  } catch {}
  try {
    const s = (await $.settings.read()) as { mcpServers?: unknown }
    const v = s.mcpServers
    if (Array.isArray(v)) for (const x of v) if (typeof x === 'string') names.add(x)
    else if (v && typeof v === 'object') for (const n of Object.keys(v)) names.add(n)
  } catch {}
  return [...names].sort()
}

function elapsed(since: number, now: number): string {
  const s = Math.max(0, Math.round((now - since) / 1000))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  return h > 0 ? `${h}h ${m}m` : `${m}m`
}

// Rate-limit resets come as ISO in UTC; show the local clock, and the day when it is not today.
function fmtReset(iso: string, now: number): string {
  const t = new Date(iso)
  if (Number.isNaN(t.getTime())) return iso
  const sameDay = new Date(now).toDateString() === t.toDateString()
  const hm = `${String(t.getHours()).padStart(2, '0')}:${String(t.getMinutes()).padStart(2, '0')}`
  return sameDay ? hm : `${t.getDate()}.${String(t.getMonth() + 1).padStart(2, '0')} ${hm}`
}

function fmtTokens(n: number | undefined): string {
  if (n === undefined) return '–'
  return n >= 1000 ? `${(n / 1000).toFixed(n >= 100000 ? 0 : 1)}K` : String(n)
}

function bar(pct: number, cells: number): string {
  const filled = Math.round((cells * pct) / 100)
  return '━'.repeat(filled) + '─'.repeat(Math.max(0, cells - filled))
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'tool',
      description: 'Pivo: tool rows — all / important only / none',
      argumentHint: '[all | important | none]',
      immediate: true,
    })
    const stored = await $.store.get('tools')
    if (stored === 'all' || stored === 'important' || stored === 'none') await update($, tools, () => stored)
    await $.command.register({
      name: 'accent',
      description: 'Pivo: your messages in the theme accent colour on/off (always bold)',
      argumentHint: '[on | off]',
      immediate: true,
    })
    if ((await $.store.get('accent')) === true) await update($, accent, () => true)
    await $.command.register({
      name: 'sidebar',
      description: 'Pivo: show/hide the status sidebar',
      immediate: true,
    })
    if ((await $.store.get('sidebar')) === true) await openSidebar($)

    return next(e)
  })

  on('command.run', { command: 'tool' }, async ($, e) => {
    const arg = e.args.trim().toLowerCase()
    const current = await read($, tools)
    const next = (MODES as string[]).includes(arg) ? (arg as ToolMode) : MODES[(MODES.indexOf(current) + 1) % MODES.length]
    await update($, tools, () => next)
    await $.store.set('tools', next)
    $.ui.invalidate('ui.render')
    $.ui.toast(`Tools: ${next === 'all' ? 'все' : next === 'important' ? 'только важные' : 'скрыты'}`)
    return {}
  })

  // Tool rows under /tool: a hidden row draws as an empty box.
  on('ui.render', { component: 'ToolUse' }, async ($, e, next) => {
    const mode = await read($, tools)
    if (!isHidden(mode, e.props.tool, e.props.isErrored)) return next(e)
    const { Box } = $.ui.resolve(e)
    return <Box />
  })
  on('ui.render', { component: 'ToolResult' }, async ($, e, next) => {
    const mode = await read($, tools)
    if (!isHidden(mode, e.props.tool, e.props.isErrored)) return next(e)
    const { Box } = $.ui.resolve(e)
    return <Box />
  })
  on('ui.render', { component: 'ToolGroup' }, async ($, e, next) => {
    const mode = await read($, tools)
    if (mode === 'all') return next(e)
    const shown = e.props.calls.some(c => !isHidden(mode, c.tool, c.isErrored))
    if (shown) return next(e)
    const { Box } = $.ui.resolve(e)
    return <Box />
  })

  on('command.run', { command: 'accent' }, async ($, e) => {
    const arg = e.args.trim().toLowerCase()
    const current = await read($, accent)
    const next = arg === 'on' ? true : arg === 'off' ? false : !current
    await update($, accent, () => next)
    await $.store.set('accent', next)
    $.ui.invalidate('ui.render')
    $.ui.toast(next ? 'Твои сообщения: жирные, цвет темы' : 'Твои сообщения: жирные, обычный цвет')
    return {}
  })

  on('command.run', { command: 'sidebar' }, async ($, e) => {
    if (!e.presentation.isFullscreen) {
      return { text: 'Сайдбар докуется только в fullscreen-режиме ("tui": "fullscreen").' }
    }
    const { isOpen } = await read($, side)
    if (isOpen) {
      await $.ui.close({ id: PANE })
      await update($, side, () => ({ isOpen: false }))
      await $.store.set('sidebar', false)
      return {}
    }
    await openSidebar($)
    return {}
  })

  on('ui.close', async ($, e, next) => {
    if (e.id === PANE) {
      await update($, side, () => ({ isOpen: false }))
      await $.store.set('sidebar', false)
    }
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    if (e.tool === 'TodoWrite') {
      const list = (e as { todos?: unknown }).todos
      if (Array.isArray(list)) {
        await update($, todos, () =>
          list.map(t => ({
            content: String((t as Todo).content ?? ''),
            status: String((t as Todo).status ?? 'pending'),
          })),
        ).catch(() => undefined)
      }
    }
    const ran = await next(e)
    await update($, tick, n => n + 1)
    return ran
  })

  on('turn.complete', async ($, e, next) => {
    await update($, tick, n => n + 1)
    return next(e)
  })

  // The person's own prompts in bold, like Pivo and the desktop app; rows the
  // engine frames (notifications, peers, collapsed rows) keep its drawing.
  on('ui.render', { component: 'UserMessage' }, async ($, e, next) => {
    const p = e.props as { text?: string; origin?: { kind?: string }; task?: unknown; from?: unknown; isExpanded?: boolean }
    const isPlain = typeof p.text === 'string' && p.task === undefined && p.from === undefined
      && (p.origin?.kind === undefined || p.origin.kind === 'composer' || p.origin.kind === 'unclassified')
    if (!isPlain) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    const isAccent = await read($, accent)
    return (
      <Box paddingX={1}>
        <Text bold color={isAccent ? 'claude' : undefined} backgroundColor="userMessageBackground" wrap="wrap">
          {'> ' + p.text}
        </Text>
      </Box>
    )
  })

  // The sidebar: what Pivo shows on the right.
  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    await read($, tick)
    const list = await read($, todos)
    const [usage, model, cwd, now, mcp] = await Promise.all([
      $.session.usage(),
      $.session.model(),
      $.session.cwd(),
      $.clock.now(),
      mcpServers($),
    ])
    const ctx = usage.context
    const ctxPct = ctx.percent ?? (ctx.tokens !== undefined ? Math.round((ctx.tokens / ctx.window) * 100) : undefined)
    const width = Math.max(10, e.props.bodyColumns - 2)

    return (
      <Box flexDirection="column" paddingX={1}>
        <Text bold>{model}</Text>
        <Text dimColor>{elapsed(usage.startedAt, now)} в сессии · {new Date(now).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}</Text>

        <Box marginTop={1} flexDirection="column">
          <Text bold>Context</Text>
          <Text>
            {fmtTokens(ctx.tokens)} / {fmtTokens(ctx.window)}
            {ctxPct !== undefined ? `  ${ctxPct}%` : ''}
          </Text>
          {ctxPct !== undefined && <Text color="claude">{bar(ctxPct, Math.min(width, 30))}</Text>}
          {usage.cost && <Text dimColor>${usage.cost.usd.toFixed(2)} spent</Text>}
        </Box>

        {usage.rateLimits.length > 0 && (
          <Box marginTop={1} flexDirection="column">
            <Text bold>Limits</Text>
            {usage.rateLimits.map(r => (
              <Text>
                <Text dimColor>{r.kind} </Text>
                {Math.round(r.percentUsed)}%
                {r.resetsAt ? <Text dimColor> · до {fmtReset(r.resetsAt, now)}</Text> : null}
              </Text>
            ))}
          </Box>
        )}

        <Box marginTop={1} flexDirection="column">
          <Text bold>Todo</Text>
          {list.length === 0 && <Text dimColor>пусто</Text>}
          {list.map(t => (
            <Text dimColor={t.status === 'completed'} wrap="truncate-end">
              {t.status === 'completed' ? '[✓] ' : t.status === 'in_progress' ? '[▶] ' : '[ ] '}
              {t.content}
            </Text>
          ))}
        </Box>

        {mcp.length > 0 && (
          <Box marginTop={1} flexDirection="column">
            <Text bold>MCP <Text dimColor>· настроены</Text></Text>
            {mcp.map(name => (
              <Text>
                <Text dimColor>• </Text>
                {name}
              </Text>
            ))}
          </Box>
        )}

        <Box marginTop={1}>
          <Text dimColor wrap="truncate-start">{cwd}</Text>
        </Box>
      </Box>
    )
  })
}
