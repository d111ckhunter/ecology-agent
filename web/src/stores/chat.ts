// 会话与聊天状态
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  createSession as apiCreateSession,
  listMessages,
  listSessions,
  streamChat,
} from '@/api/client'
import type { ChatMsg, MessageItem, SessionItem } from '@/types'

let seq = 0
function nextId(prefix = 'local'): string {
  return `${prefix}-${++seq}-${Date.now()}`
}

/** 后端 MessageItem -> 统一展示模型 ChatMsg */
function toChatMsg(m: MessageItem): ChatMsg {
  return {
    id: String(m.id),
    role: m.role,
    content: m.content ?? '',
    sql: m.sql,
    table: null, // 历史消息不存表格事件；如需展示可用 result_summary（略）
    status: m.role === 'user' ? 'done' : m.error ? 'error' : 'done',
    error: m.error,
  }
}

export const useChatStore = defineStore('chat', () => {
  // ---------- state ----------
  const sessions = ref<SessionItem[]>([])
  const activeSessionId = ref<string | null>(null)
  const messages = ref<ChatMsg[]>([])
  const sending = ref(false)
  const sessionsLoading = ref(false)
  const error = ref('')

  // ---------- getters ----------
  const activeSession = computed(
    () => sessions.value.find((s) => s.id === activeSessionId.value) ?? null,
  )

  // ---------- actions ----------
  async function loadSessions() {
    sessionsLoading.value = true
    try {
      const data = await listSessions(100)
      sessions.value = data.items
      if (!activeSessionId.value && data.items.length > 0) {
        await selectSession(data.items[0].id)
      }
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      sessionsLoading.value = false
    }
  }

  async function loadMessages(sessionId: string) {
    const raw = await listMessages(sessionId)
    messages.value = raw.map(toChatMsg)
  }

  async function newSession(question?: string) {
    const s = await apiCreateSession()
    sessions.value.unshift(s)
    activeSessionId.value = s.id
    messages.value = []
    if (question && question.trim()) {
      await ask(question.trim())
    }
  }

  async function selectSession(id: string) {
    if (sending.value) return
    if (id === activeSessionId.value && messages.value.length > 0) return
    activeSessionId.value = id
    await loadMessages(id)
  }

  /** 向当前会话提问（SSE 流式更新本地 pending 消息） */
  async function ask(question: string) {
    if (sending.value) return
    if (!activeSessionId.value) {
      await newSession(question)
      return
    }
    const sessionId = activeSessionId.value
    sending.value = true
    error.value = ''

    messages.value.push({
      id: nextId('user'),
      role: 'user',
      content: question,
      sql: null,
      table: null,
      status: 'done',
      error: null,
    })
    const pending: ChatMsg = {
      id: nextId('asst'),
      role: 'assistant',
      content: '',
      sql: null,
      table: null,
      status: 'thinking',
      error: null,
    }
    messages.value.push(pending)

    try {
      await streamChat(sessionId, question, (ev) => {
        switch (ev.type) {
          case 'status':
            pending.status = ev.stage === 'composing' ? 'running' : 'thinking'
            break
          case 'sql':
            pending.sql = ev.sql
            pending.status = 'running'
            break
          case 'table':
            pending.table = ev
            pending.status = 'running'
            break
          case 'answer':
            pending.content = ev.text
            break
          case 'error':
            pending.status = 'error'
            pending.error = ev.message
            break
          case 'done':
            pending.status = ev.ok ? 'done' : 'error'
            break
        }
      })
      if (pending.status === 'thinking' || pending.status === 'running') {
        pending.status = 'done'
      }
    } catch (e: unknown) {
      pending.status = 'error'
      pending.error = (e as Error).message
    } finally {
      sending.value = false
      // 流结束后把该会话持久化消息拉回，替换本地占位（保证刷新一致）
      try {
        const raw = await listMessages(sessionId)
        messages.value = raw.map(toChatMsg)
      } catch { /* 保留本地状态 */ }
    }
  }

  return {
    sessions,
    activeSessionId,
    activeSession,
    messages,
    sending,
    sessionsLoading,
    error,
    loadSessions,
    loadMessages,
    newSession,
    selectSession,
    ask,
  }
})
