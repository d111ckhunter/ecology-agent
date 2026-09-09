<template>
  <div class="app-shell">
    <!-- 顶部栏 -->
    <header class="topbar">
      <div class="topbar__brand">
        <div class="logo">🌿</div>
        <div class="brand-text">
          <span class="brand-name">ecology-agent</span>
          <span class="brand-sub">生态监测 · 数据问答</span>
        </div>
      </div>
      <div class="topbar__right">
        <!-- SQL 显示开关（默认关闭） -->
        <el-tooltip content="显示/隐藏 SQL" placement="bottom">
          <div class="sql-toggle">
            <span class="sql-toggle__label">SQL</span>
            <el-switch v-model="sqlVisible" size="small" />
          </div>
        </el-tooltip>
        <span class="mode-chip" :class="chat.sending ? 'is-busy' : ''">
          <span class="dot" :class="chat.sending ? 'dot--busy' : 'dot--ok'"></span>
          {{ chat.sending ? '生成中' : '在线' }}
        </span>
      </div>
    </header>

    <div class="workspace">
      <!-- 左侧会话列表 -->
      <aside class="sidebar">
        <el-button class="new-btn" type="primary" :icon="Plus" @click="onNew">
          新建会话
        </el-button>

        <div class="sidebar__label">历史会话</div>
        <div v-loading="chat.sessionsLoading" class="session-list">
          <div
            v-for="s in chat.sessions"
            :key="s.id"
            class="session-item"
            :class="{ active: s.id === chat.activeSessionId }"
            @click="chat.selectSession(s.id)"
          >
            <el-icon class="session-icon"><ChatDotRound /></el-icon>
            <span class="session-title">{{ s.title || '未命名会话' }}</span>
            <el-popconfirm
              title="确定删除该会话？"
              confirm-button-text="删除"
              cancel-button-text="取消"
              width="220"
              @confirm="chat.removeSession(s.id)"
            >
              <template #reference>
                <el-icon
                  class="session-delete"
                  title="删除会话"
                  @click.stop
                ><Delete /></el-icon>
              </template>
            </el-popconfirm>
          </div>
          <el-empty
            v-if="!chat.sessionsLoading && chat.sessions.length === 0"
            description="暂无会话"
            :image-size="60"
          />
        </div>
      </aside>

      <!-- 右侧聊天区 -->
      <main class="chat">
        <ChatMessages @suggest="onSend" />
        <ChatInput :sending="chat.sending" @send="onSend" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { ChatDotRound, Delete, Plus } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'
import ChatMessages from '@/components/ChatMessages.vue'
import ChatInput from '@/components/ChatInput.vue'

const chat = useChatStore()

const sqlVisible = computed({
  get: () => chat.showSql,
  set: (v: boolean) => chat.setShowSql(v),
})

onMounted(() => {
  chat.loadSessions()
})

async function onNew() {
  await chat.newSession()
}

async function onSend(q: string) {
  if (chat.sending) return
  if (chat.activeSessionId) {
    await chat.ask(q)
  } else {
    await chat.newSession(q)
  }
}
</script>

<style scoped>
.app-shell {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 14px 18px 18px;
  max-width: 1480px;
  margin: 0 auto;
}

/* ---------- 顶部栏 ---------- */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 6px 14px;
}
.topbar__brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: linear-gradient(135deg, #2f9e6e, #3370ff);
  box-shadow: 0 4px 10px rgba(51, 112, 255, 0.28);
}
.brand-text {
  display: flex;
  flex-direction: column;
}
.brand-name {
  font-size: 16px;
  font-weight: 700;
  color: #16233a;
  letter-spacing: 0.2px;
}
.brand-sub {
  font-size: 11px;
  color: #7a8ba5;
}
.topbar__right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.sql-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #4a6a92;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #dde6f2;
  padding: 5px 12px;
  border-radius: 999px;
  backdrop-filter: blur(4px);
  cursor: pointer;
}
.sql-toggle__label {
  font-weight: 600;
  letter-spacing: 0.5px;
}
.mode-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #4a6a92;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #dde6f2;
  padding: 4px 12px;
  border-radius: 999px;
  backdrop-filter: blur(4px);
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.dot--ok {
  background: #2fbf71;
  box-shadow: 0 0 0 3px rgba(47, 191, 113, 0.18);
}
.dot--busy {
  background: #ffb020;
  animation: pulse 1s infinite;
}
@keyframes pulse {
  50% {
    opacity: 0.35;
  }
}

/* ---------- 工作区 ---------- */
.workspace {
  flex: 1;
  display: flex;
  min-height: 0;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow:
    0 12px 40px rgba(31, 62, 105, 0.12),
    0 2px 8px rgba(31, 62, 105, 0.06);
}

/* ---------- 侧栏 ---------- */
.sidebar {
  width: 270px;
  min-width: 270px;
  background: linear-gradient(180deg, #f7fafd, #f0f5fb);
  border-right: 1px solid #e6edf5;
  display: flex;
  flex-direction: column;
  padding: 14px 12px;
}
.new-btn {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(51, 112, 255, 0.22);
}
.sidebar__label {
  font-size: 11px;
  color: #94a5bd;
  letter-spacing: 1px;
  margin: 16px 6px 8px;
  font-weight: 600;
}
.session-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.session-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  color: #33465e;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}
.session-icon {
  color: #8fa3bd;
  font-size: 15px;
  flex-shrink: 0;
}
.session-item:hover {
  background: #fff;
  border-color: #e3ecf6;
  box-shadow: 0 2px 8px rgba(31, 62, 105, 0.06);
}
.session-item.active {
  background: linear-gradient(135deg, #eaf1ff, #e5f6ee);
  border-color: rgba(51, 112, 255, 0.25);
  color: #2b5ce6;
  font-weight: 600;
}
.session-item.active .session-icon {
  color: #3370ff;
}
.session-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.session-delete {
  opacity: 0;
  color: #b6c2d4;
  font-size: 14px;
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.15s ease;
}
.session-item:hover .session-delete {
  opacity: 1;
}
.session-delete:hover {
  color: #f56c6c;
}

/* ---------- 聊天区 ---------- */
.chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #fbfcfe;
}
</style>
