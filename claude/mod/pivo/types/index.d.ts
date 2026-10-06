export type Side = { isOpen: boolean }
export type ToolMode = 'all' | 'important' | 'none'
export type Todo = { content: string; status: string }

declare module 'claude-code' {
  interface PluginState {
    pivo: { side: Side; todos: Todo[]; tick: number; tools: ToolMode }
  }
}
