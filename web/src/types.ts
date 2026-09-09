// 与后端 app/schemas/api.py + SSE 协议对齐的类型定义

export interface SessionItem {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface MessageItem {
  id: number
  session_id: string
  role: 'user' | 'assistant'
  content: string | null
  sql: string | null
  result_summary: string | null
  error: string | null
  created_at: string
}

// ---- SSE 事件（与 app/services/agent_service.py 对齐）----
export interface StatusEvent { type: 'status'; stage: string }
export interface SqlEvent { type: 'sql'; sql: string; thinking?: string }
export interface TableEvent {
  type: 'table'
  columns: string[]
  rows: (string | number | null)[][]
  truncated: boolean
  elapsed?: number
}
export interface AnswerEvent { type: 'answer'; text: string }
export interface ErrorEvent { type: 'error'; message: string }
export interface DoneEvent {
  type: 'done'
  session_id: string
  message_id?: number
  ok: boolean
}

export type ChatEvent =
  | StatusEvent
  | SqlEvent
  | TableEvent
  | AnswerEvent
  | ErrorEvent
  | DoneEvent

/** 统一的消息展示模型：历史消息与"流式中"消息同构 */
export interface ChatMsg {
  id: string
  role: 'user' | 'assistant'
  content: string
  sql: string | null
  table: TableEvent | null
  status: 'done' | 'running' | 'thinking' | 'error'
  error: string | null
}
