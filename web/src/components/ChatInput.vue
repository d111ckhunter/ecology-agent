<template>
  <div class="input-area">
    <div class="input-card">
      <el-input
        v-model="text"
        type="textarea"
        :rows="2"
        resize="none"
        :disabled="sending"
        placeholder="输入你的问题，例如：2024 年哪个测站氨氮最高？（Enter 发送，Shift+Enter 换行）"
        @keydown.enter.exact.prevent="send"
      />
      <div class="input-actions">
        <span class="hint">
          <el-icon class="hint-icon"><InfoFilled /></el-icon>
          支持多轮追问，如「那 2024 年呢？」
        </span>
        <el-button
          type="primary"
          :loading="sending"
          :disabled="!text.trim() || sending"
          class="send-btn"
          @click="send"
        >
          {{ sending ? '生成中' : '发送' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'

defineProps<{ sending: boolean }>()
const emit = defineEmits<{ send: [question: string] }>()

const text = ref('')

function send() {
  const q = text.value.trim()
  if (!q) return
  text.value = ''
  emit('send', q)
}
</script>

<style scoped>
.input-area {
  padding: 8px 6% 18px;
  background: linear-gradient(180deg, transparent, #fbfcfe 30%);
}
.input-card {
  max-width: 860px;
  margin: 0 auto;
  background: #fff;
  border: 1px solid #dde6f2;
  border-radius: 16px;
  padding: 10px 12px 8px;
  box-shadow: 0 8px 24px rgba(31, 62, 105, 0.1);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.input-card:focus-within {
  border-color: #3370ff;
  box-shadow: 0 8px 28px rgba(51, 112, 255, 0.16);
}

.input-card :deep(.el-textarea__inner) {
  border: none;
  box-shadow: none;
  background: transparent;
  padding: 6px 8px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
}
.input-card :deep(.el-textarea__inner:focus) {
  box-shadow: none;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  padding: 0 4px;
}
.hint {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #9aa8bd;
}
.hint-icon {
  font-size: 13px;
}
.send-btn {
  border-radius: 10px;
  padding: 8px 22px;
}
</style>
