<template>
  <div class="messages" ref="scrollRef">
    <!-- 空状态：欢迎 + 示例问题 -->
    <div v-if="messages.length === 0" class="welcome">
      <div class="welcome__icon">🌊</div>
      <h2 class="welcome__title">你好，我是生态数据助手</h2>
      <p class="welcome__desc">
        用自然语言查询生态环境监测数据，试试下面的问题：
      </p>
      <div class="suggest-grid">
        <button
          v-for="s in suggestions"
          :key="s"
          class="suggest-item"
          @click="$emit('suggest', s)"
        >
          {{ s }}
        </button>
      </div>
    </div>

    <!-- 消息流 -->
    <template v-else>
      <div
        v-for="m in messages"
        :key="m.id"
        class="row"
        :class="m.role === 'user' ? 'row--user' : 'row--assistant'"
      >
        <!-- 用户：先气泡后头像 -->
        <template v-if="m.role === 'user'">
          <div class="bubble bubble--user">
            <div class="plain">{{ m.content }}</div>
          </div>
          <div class="avatar avatar--user">
            <el-icon><User /></el-icon>
          </div>
        </template>

        <!-- 助手：先头像后气泡 -->
        <template v-else>
          <div class="avatar avatar--ai">
            <el-icon><MagicStick /></el-icon>
          </div>
          <div class="bubble bubble--assistant">
            <!-- 思考中 -->
            <div v-if="m.status === 'thinking' && !m.sql && !m.content" class="status-line">
              <span class="typing-dots"><i></i><i></i><i></i></span>
              正在理解并生成 SQL…
            </div>

            <!-- SQL 展示 -->
            <div v-if="m.sql" class="sql-block">
              <div class="sql-block__head">
                <span class="sql-label">SQL</span>
                <span class="sql-actions">
                  <el-button link size="small" @click="copied = m.id; copySql(m.sql!)">
                    {{ copied === m.id ? '✓ 已复制' : '复制' }}
                  </el-button>
                  <el-button link size="small" @click="toggleCollapse(m.id)">
                    {{ collapsed.has(m.id) ? '展开' : '收起' }}
                  </el-button>
                </span>
              </div>
              <pre v-show="!collapsed.has(m.id)" class="sql-code"
                ><code class="hljs" v-html="highlightSql(m.sql)"></code></pre>
            </div>

            <!-- 结果表格 -->
            <div v-if="m.table && m.table.columns.length" class="table-block">
              <el-table
                :data="rowsAsObjects(m.table)"
                size="small"
                border
                max-height="300"
                :header-cell-style="{ background: '#f3f7fc', color: '#4a6080' }"
              >
                <el-table-column
                  v-for="col in m.table.columns"
                  :key="col"
                  :prop="col"
                  :label="col"
                  min-width="110"
                />
              </el-table>
              <div v-if="m.table.truncated" class="truncate-note">
                结果超过 200 行，仅展示前 200 行
              </div>
            </div>

            <!-- 回答文本 -->
            <div v-if="m.content" class="answer-text">{{ m.content }}</div>

            <!-- 错误 -->
            <div v-if="m.status === 'error' && m.error" class="error-box">
              <el-icon><WarningFilled /></el-icon>
              <span>{{ m.error }}</span>
            </div>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { MagicStick, User, WarningFilled } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'
import { highlightSql } from '@/utils/format'
import type { TableEvent } from '@/types'

defineEmits<{ suggest: [question: string] }>()

const chat = useChatStore()
const { messages } = storeToRefs(chat)

const scrollRef = ref<HTMLElement | null>(null)
const collapsed = ref<Set<string>>(new Set())
const copied = ref<string | null>(null)

const suggestions = [
  '2024 年哪个测站氨氮最高？',
  '对比各河段的鱼类物种数',
  '2023 年水温最高的月份是？',
]

function toggleCollapse(id: string) {
  const s = new Set(collapsed.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  collapsed.value = s
}

function copySql(sql: string) {
  navigator.clipboard?.writeText(sql)
}

function rowsAsObjects(t: TableEvent) {
  return t.rows.map((r) => {
    const o: Record<string, unknown> = {}
    t.columns.forEach((c, idx) => {
      o[c] = r[idx]
    })
    return o
  })
}

async function scrollToBottom() {
  await nextTick()
  if (scrollRef.value) {
    scrollRef.value.scrollTop = scrollRef.value.scrollHeight
  }
}

watch(
  () =>
    messages.value
      .map((m) => `${m.id}|${m.content?.length ?? 0}|${m.status ?? ''}|${m.sql ?? ''}`)
      .join('~'),
  () => scrollToBottom(),
)
</script>

<style scoped>
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 26px 6% 18px;
  display: flex;
  flex-direction: column;
}

/* ---------- 空状态 ---------- */
.welcome {
  margin: auto;
  text-align: center;
  animation: fade-up 0.4s ease;
}
.welcome__icon {
  font-size: 52px;
  margin-bottom: 8px;
}
.welcome__title {
  font-size: 21px;
  font-weight: 700;
  color: #1d2b45;
  margin-bottom: 6px;
}
.welcome__desc {
  font-size: 13px;
  color: #7a8ba5;
  margin-bottom: 20px;
}
.suggest-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
  max-width: 720px;
  margin: 0 auto;
}
.suggest-item {
  padding: 12px 16px;
  background: #fff;
  border: 1px solid #dde6f2;
  border-radius: 12px;
  font-size: 13px;
  color: #33465e;
  cursor: pointer;
  transition: all 0.18s ease;
  box-shadow: 0 1px 4px rgba(31, 62, 105, 0.04);
}
.suggest-item:hover {
  border-color: #3370ff;
  color: #2b5ce6;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(51, 112, 255, 0.15);
}

/* ---------- 消息行 ---------- */
.row {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  animation: fade-up 0.3s ease;
}
.row--user {
  justify-content: flex-end;
}
.row--assistant {
  justify-content: flex-start;
}

/* ---------- 头像 ---------- */
.avatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  margin-top: 2px;
}
.avatar--user {
  background: linear-gradient(135deg, #3370ff, #5b8cff);
  color: #fff;
  box-shadow: 0 3px 8px rgba(51, 112, 255, 0.3);
}
.avatar--ai {
  background: linear-gradient(135deg, #2f9e6e, #54c08b);
  color: #fff;
  box-shadow: 0 3px 8px rgba(47, 158, 110, 0.3);
}

/* ---------- 气泡 ---------- */
.bubble {
  max-width: 82%;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.75;
  word-break: break-word;
}
.bubble--user {
  background: linear-gradient(135deg, #3370ff, #4a84ff);
  color: #fff;
  border-radius: 16px 16px 4px 16px;
  box-shadow: 0 6px 16px rgba(51, 112, 255, 0.22);
}
.bubble--assistant {
  background: #fff;
  border: 1px solid #e3ecf6;
  border-radius: 4px 16px 16px 16px;
  box-shadow: 0 4px 14px rgba(31, 62, 105, 0.07);
  color: #2b3850;
}
.plain {
  white-space: pre-wrap;
}
.answer-text {
  white-space: pre-wrap;
}

/* ---------- 思考动画 ---------- */
.status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #7a8ba5;
  font-size: 13px;
}
.typing-dots i {
  display: inline-block;
  width: 6px;
  height: 6px;
  margin-right: 3px;
  background: #8fa3bd;
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}
.typing-dots i:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-dots i:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes bounce {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-4px);
    opacity: 1;
  }
}

/* ---------- SQL 代码块 ---------- */
.sql-block {
  margin: 4px 0 10px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #20293a;
  font-family: inherit;
}
.sql-block__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #20293a;
  padding: 4px 12px;
}
.sql-label {
  font-size: 11px;
  font-weight: 700;
  color: #ffd479;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.sql-label::before {
  content: '◈';
  font-size: 10px;
}
.sql-actions :deep(.el-button) {
  color: #9db1c8;
  font-size: 12px;
}
.sql-code {
  background: #0d1117;
  margin: 0;
  padding: 12px 14px;
  font-size: 12.5px;
  line-height: 1.7;
  overflow-x: auto;
  font-family: 'JetBrains Mono', 'Fira Code', Consolas, Menlo, monospace;
}
.sql-code :deep(code.hljs) {
  background: transparent;
  padding: 0;
}

/* ---------- 表格 ---------- */
.table-block {
  margin: 4px 0 10px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e6edf5;
}
.truncate-note {
  font-size: 12px;
  color: #b8890b;
  padding: 6px 10px;
  background: #fffbea;
}

/* ---------- 错误 ---------- */
.error-box {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  color: #f56c6c;
  font-size: 13px;
  background: #fef0f0;
  border-radius: 8px;
  padding: 8px 10px;
  margin-top: 4px;
}
</style>
