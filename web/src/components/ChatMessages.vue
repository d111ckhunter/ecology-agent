<template>
  <div class="messages" ref="scrollRef">
    <el-empty v-if="messages.length === 0" description="问点什么吧，例如：2024年哪个测站氨氮最高？" :image-size="80" />
    <div
      v-for="m in messages"
      :key="m.id"
      class="row"
      :class="m.role === 'user' ? 'row--user' : 'row--assistant'"
    >
      <div class="bubble" :class="m.role === 'user' ? 'bubble--user' : 'bubble--assistant'">
        <!-- 用户消息：纯文本 -->
        <template v-if="m.role === 'user'">
          <div class="plain">{{ m.content }}</div>
        </template>

        <!-- 助手消息 -->
        <template v-else>
          <!-- 思考中（尚无 SQL/回答） -->
          <div v-if="m.status === 'thinking' && !m.sql && !m.content" class="status-line">
            <el-icon class="is-loading"><Loading /></el-icon> 正在理解问题并生成 SQL…
          </div>

          <!-- SQL 展示 -->
          <div v-if="m.sql" class="sql-block">
            <div class="sql-block__head">
              <span class="sql-label">SQL</span>
              <span class="sql-actions">
                <el-button link size="small" @click="copied = m.id; copySql(m.sql!)">
                  {{ copied === m.id ? '已复制' : '复制' }}
                </el-button>
                <el-button link size="small" @click="toggleCollapse(m.id)">
                  {{ collapsed.has(m.id) ? '展开' : '收起' }}
                </el-button>
              </span>
            </div>
            <pre v-show="!collapsed.has(m.id)" class="sql-code"><code v-html="highlightSql(m.sql)" /></pre>
          </div>

          <!-- 结果表格 -->
          <div v-if="m.table && m.table.columns.length" class="table-block">
            <el-table
              :data="rowsAsObjects(m.table)"
              size="small"
              border
              max-height="320"
            >
              <el-table-column
                v-for="col in m.table.columns"
                :key="col"
                :prop="col"
                :label="col"
                min-width="110"
              />
            </el-table>
            <div v-if="m.table.truncated" class="truncate-note">结果超过 200 行，仅展示前 200 行</div>
          </div>

          <!-- 回答文本 -->
          <div v-if="m.content" class="answer-text">{{ m.content }}</div>

          <!-- 错误 -->
          <div v-if="m.status === 'error' && m.error" class="error-box">
            <el-icon><WarningFilled /></el-icon>
            <span>{{ m.error }}</span>
          </div>

          <!-- 光标（仍在生成） -->
          <span v-if="m.status === 'running' || (m.status === 'thinking' && m.sql)" class="cursor">▋</span>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Loading, WarningFilled } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'
import { highlightSql } from '@/utils/format'
import type { TableEvent } from '@/types'

const chat = useChatStore()
const { messages } = storeToRefs(chat)

const scrollRef = ref<HTMLElement | null>(null)
const collapsed = ref<Set<string>>(new Set())
const copied = ref<string | null>(null)

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

// 消息数/内容变化时自动滚底
watch(
  () => messages.value.map((m) => m.id + (m.content?.length ?? 0) + (m.status ?? '')).join('|'),
  () => scrollToBottom(),
)
</script>

<style scoped>
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 18px 22px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.row {
  display: flex;
}
.row--user {
  justify-content: flex-end;
}
.row--assistant {
  justify-content: flex-start;
}
.bubble {
  max-width: 82%;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;
}
.bubble--user {
  background: #409eff;
  color: #fff;
  border-top-right-radius: 2px;
}
.bubble--assistant {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-top-left-radius: 2px;
}
.plain {
  white-space: pre-wrap;
}
.status-line {
  color: #909399;
  display: flex;
  align-items: center;
  gap: 6px;
}
.sql-block {
  margin-bottom: 8px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
}
.sql-block__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f5f7fa;
  padding: 2px 8px;
  border-bottom: 1px solid #ebeef5;
}
.sql-label {
  font-size: 12px;
  font-weight: 600;
  color: #67c23a;
}
.sql-actions {
  display: flex;
}
.sql-code {
  background: #f8f8f8;
  margin: 0;
  padding: 8px 10px;
  font-size: 12px;
  line-height: 1.6;
  overflow-x: auto;
}
.table-block {
  margin-bottom: 8px;
}
.truncate-note {
  font-size: 12px;
  color: #e6a23c;
  margin-top: 4px;
}
.answer-text {
  white-space: pre-wrap;
}
.error-box {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  color: #f56c6c;
  font-size: 13px;
}
.cursor {
  display: inline-block;
  width: 6px;
  margin-left: 2px;
  animation: blink 1s step-start infinite;
  color: #409eff;
}
@keyframes blink {
  50% { opacity: 0; }
}
</style>
