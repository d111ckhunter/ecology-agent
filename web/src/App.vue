<template>
  <div class="layout">
    <!-- 左侧会话列表 -->
    <aside class="sidebar">
      <div class="sidebar__head">
        <div class="brand">🌊 ecology-agent</div>
        <el-button type="primary" size="small" style="width: 100%" @click="onNew">
          <el-icon><Plus /></el-icon>&nbsp;新建会话
        </el-button>
      </div>
      <div v-loading="chat.sessionsLoading" class="session-list">
        <div
          v-for="s in chat.sessions"
          :key="s.id"
          class="session-item"
          :class="{ active: s.id === chat.activeSessionId }"
          @click="chat.selectSession(s.id)"
        >
          <span class="session-title">{{ s.title || '未命名会话' }}</span>
        </div>
        <el-empty v-if="!chat.sessionsLoading && chat.sessions.length === 0" description="暂无会话" :image-size="60" />
      </div>
    </aside>

    <!-- 右侧聊天区 -->
    <main class="chat">
      <ChatMessages />
      <ChatInput :sending="chat.sending" @send="onSend" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'
import ChatMessages from '@/components/ChatMessages.vue'
import ChatInput from '@/components/ChatInput.vue'

const chat = useChatStore()

onMounted(() => {
  chat.loadSessions()
})

async function onNew() {
  await chat.newSession()
}

async function onSend(q: string) {
  if (chat.activeSessionId) {
    await chat.ask(q)
  } else {
    await chat.newSession(q)
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100%;
}
.sidebar {
  width: 280px;
  min-width: 280px;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}
.sidebar__head {
  padding: 14px 12px 10px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.brand {
  font-weight: 600;
  font-size: 15px;
  color: #409eff;
}
.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px;
}
.session-item {
  padding: 9px 10px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 2px;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.session-item:hover {
  background: #f5f7fa;
}
.session-item.active {
  background: #ecf5ff;
  color: #409eff;
  font-weight: 500;
}
.chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
</style>
