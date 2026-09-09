// 会话与聊天状态
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  createSession as apiCreateSession,
  deleteSession as apiDeleteSession,
  listMessages,
  listSessions,
  streamChat,
} from '@/api/client'
import type { ChatMsg, MessageItem, SessionItem } from '@/types'

const SHOW_SQL_KEY = 'ecology.showSql'

let seq = 0
function nextId(prefix = 'local'): string {
  return `${prefix}-${++seq}-${Date.now()}`
}

function loadShowSql(): boolean {
  return localStorage.getItem(SHOW_SQL_KEY) === '1'
}

/** 后端 MessageItem -> 统一展示模型 ChatMsg */
function toChatMsg(m: MessageItem): ChatMsg {
  return {
    id: String(m.id),
    role: m.role,
    content: m.content ?? '',
    sql: m.sql,
    table: null, // 历史消息不落表格事件（仅存 result_summary）
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
  // 是否展示 SQL 代码块（默认关闭，用户可在界面切换，记忆在 localStorage）
  const showSql = ref(loadShowSql())

  // ---------- getters ----------
  const activeSession = computed(
    () => sessions.value.find((s) => s.id === activeSessionId.value) ?? null,
  )

  // ---------- actions ----------
  function setShowSql(v: boolean) {
    showSql.value = v
    localStorage.setItem(SHOW_SQL_KEY, v ? '1' : '0')
  }

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

  /** 删除会话；若删除的是当前会话则自动切到最近一个（或空态） */
  async function removeSession(id: string) {
    const idx = sessions.value.findIndex((s) => s.id === id)
    if (idx < 0) return
    try {
      await apiDeleteSession(id)
    } catch (e: unknown) {
      error.value = (e as Error).message
      return
    }
    sessions.value.splice(idx, 1)
    if (activeSessionId.value === id) {
      activeSessionId.value = null
      messages.value = []
      if (sessions.value.length > 0) {
        // 切换到原位置之后的会话；越界则选第一个
        const next = sessions.value[Math.min(idx, sessions.value.length - 1)]
        await selectSession(next.id)
      }
    }
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
    // 关键：必须取回响应式数组中的 proxy 引用再修改，
    // 直接改 push 前的原始对象不会触发 Vue 视图更新（内容/状态将卡在初始值）
    const live = messages.value[messages.value.length - 1]!

    try {
      await streamChat(sessionId, question, (ev) => {
        switch (ev.type) {
          case 'status':
            if (ev.stage === 'chat_fallback') live.status = 'running'
            else live.status = ev.stage === 'composing' ? 'running' : 'thinking'
            break
          case 'sql':
            live.sql = ev.sql
            live.status = 'running'
            break
          case 'table':
            live.table = ev
            live.status = 'running'
            break
          case 'answer':
            // 兼容：一次性 answer 视为整段
            live.content += ev.text
            live.status = 'running'
            break
          case 'answer_delta':
            // v3：token 级增量，追加即可（流式期间以纯文本展示）
            live.content += ev.delta
            live.status = 'running'
            break
          case 'error':
            live.status = 'error'
            live.error = ev.message
            break
          case 'done':
            live.status = ev.ok ? 'done' : 'error'
            break
        }
      })
      if (live.status === 'thinking' || live.status === 'running') {
        live.status = 'done'
      }
    } catch (e: unknown) {
      live.status = 'error'
      live.error = (e as Error).message
    } finally {
      sending.value = false
      // 保留本地累积的完整内容/表格（服务端已持久化同内容），不整表替换以免丢失表格与增量
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
    showSql,
    setShowSql,
    loadSessions,
    loadMessages,
    newSession,
    selectSession,
    removeSession,
    ask,
  }
})
