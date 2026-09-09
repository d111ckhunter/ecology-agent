// HTTP + SSE 客户端：与后端 app/api/sessions.py 对齐
import type {
  ChatEvent,
  MessageItem,
  SessionItem,
} from '@/types'

const BASE = '/api'

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = res.statusText
    try {
      const j = await res.json()
      detail = j?.detail ?? detail
    } catch { /* ignore */ }
    throw new Error(`${res.status}: ${detail}`)
  }
  return res.json() as Promise<T>
}

export async function createSession(title = ''): Promise<SessionItem> {
  const res = await fetch(`${BASE}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })
  return handle<SessionItem>(res)
}

export async function listSessions(limit = 100): Promise<{ total: number; items: SessionItem[] }> {
  const res = await fetch(`${BASE}/sessions?limit=${limit}`)
  return handle<{ total: number; items: SessionItem[] }>(res)
}

export async function listMessages(sessionId: string): Promise<MessageItem[]> {
  const res = await fetch(`${BASE}/sessions/${sessionId}/messages`)
  return handle<MessageItem[]>(res)
}

/**
 * 提问并解析 SSE 流。由于 EventSource 不支持 POST，这里用
 * fetch + ReadableStream 手动按 SSE 协议逐帧解析，回调每类事件。
 */
export async function streamChat(
  sessionId: string,
  question: string,
  onEvent: (ev: ChatEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const res = await fetch(`${BASE}/sessions/${sessionId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
    body: JSON.stringify({ question }),
    signal,
  })
  if (!res.ok || !res.body) {
    throw new Error(`${res.status}: ${res.statusText}`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  const parseFrame = (frame: string) => {
    let eventName = 'message'
    const dataLines: string[] = []
    for (const line of frame.split('\n')) {
      if (line.startsWith('event:')) {
        eventName = line.slice(6).trim()
      } else if (line.startsWith('data:')) {
        dataLines.push(line.slice(5).trim())
      }
    }
    if (dataLines.length === 0) return
    const data = dataLines.join('\n')
    try {
      const obj = JSON.parse(data)
      if (obj && typeof obj.type === 'string') {
        onEvent(obj as ChatEvent)
      }
    } catch {
      onEvent({ type: 'error', message: `无法解析服务端事件: ${data.slice(0, 120)}` } as ChatEvent)
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      // SSE 帧以空行分隔
      let idx: number
      while ((idx = buffer.indexOf('\n\n')) >= 0) {
        const frame = buffer.slice(0, idx)
        buffer = buffer.slice(idx + 2)
        if (frame.trim()) parseFrame(frame)
      }
    }
    if (buffer.trim()) parseFrame(buffer) // 结尾帧
  } finally {
    reader.releaseLock()
  }
}
