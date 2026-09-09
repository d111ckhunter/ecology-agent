<template>
  <div class="input-bar">
    <div class="input-box">
      <el-input
        v-model="text"
        type="textarea"
        :rows="2"
        resize="none"
        :disabled="sending"
        placeholder="输入你的问题，例如：2024年哪个测站氨氮最高？ ／ 各河段鱼类物种数对比（Enter 发送，Shift+Enter 换行）"
        @keydown.enter.exact.prevent="send"
      />
      <div class="actions">
        <span class="hint">支持多轮追问，如「那 2024 年呢？」</span>
        <el-button type="primary" :loading="sending" :disabled="!text.trim() || sending" @click="send">
          {{ sending ? '生成中' : '发送' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

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
.input-bar {
  border-top: 1px solid #e4e7ed;
  background: #fff;
  padding: 12px 20px;
}
.input-box {
  max-width: 900px;
  margin: 0 auto;
}
.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}
.hint {
  font-size: 12px;
  color: #909399;
}
</style>
