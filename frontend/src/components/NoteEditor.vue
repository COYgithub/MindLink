<template>
  <div class="note-editor rounded-xl shadow-lg p-8 transition-all duration-300" :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
      <el-input
        v-model="noteTitle"
        placeholder="请输入笔记标题"
        class="text-2xl font-bold flex-1 transition-colors"
        size="large"
        :class="{ 
          'bg-transparent border-none': !isDarkMode, 
          'bg-transparent border-none text-white': isDarkMode 
        }"
      />
      <div class="flex gap-3">
        <el-button 
          @click="saveNote" 
          :loading="isSaving"
          type="primary"
          size="large"
          round
          class="bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:shadow-lg transition-all"
        >
          <el-icon class="mr-1"><Document /></el-icon>
          保存
        </el-button>
        <el-button 
          @click="cancelEdit"
          size="large"
          round
          :class="{ 
            'bg-gray-100 text-gray-800 hover:bg-gray-200': !isDarkMode, 
            'bg-gray-700 text-gray-200 hover:bg-gray-600': isDarkMode 
          }"
        >
          <el-icon class="mr-1"><Close /></el-icon>
          取消
        </el-button>
      </div>
    </div>
    
    <div class="mb-6">
      <el-input
        v-model="noteTags"
        placeholder="请输入标签，用逗号分隔"
        class="w-full rounded-lg transition-all"
        :class="{ 
          'bg-gray-50 border-gray-200': !isDarkMode, 
          'bg-gray-700 border-gray-600 text-white': isDarkMode 
        }"
      />
    </div>
    
    <div class="editor-container rounded-lg overflow-hidden">
      <el-input
        v-model="noteContent"
        type="textarea"
        :rows="25"
        placeholder="开始编写您的笔记..."
        class="w-full resize-none transition-colors"
        :class="{ 
          'bg-gray-50 border-gray-200 text-gray-800': !isDarkMode, 
          'bg-gray-700 border-gray-600 text-white': isDarkMode 
        }"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Document, Close } from '@element-plus/icons-vue'
import { useDark } from '@/composables/useDark'

/**
 * 笔记编辑器组件
 * 提供笔记的创建和编辑功能
 */

// 使用深色模式组合式函数
const { isDarkMode } = useDark()

const props = defineProps({
  noteId: {
    type: [Number, String],
    default: null
  },
  initialTitle: {
    type: String,
    default: ''
  },
  initialContent: {
    type: String,
    default: ''
  },
  initialTags: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['save', 'cancel'])

const noteTitle = ref(props.initialTitle)
const noteContent = ref(props.initialContent)
const noteTags = ref(props.initialTags.join(', '))
const isSaving = ref(false)

// 监听props变化并更新响应式变量
watch(() => props.initialTitle, (newTitle) => {
  noteTitle.value = newTitle
})

watch(() => props.initialContent, (newContent) => {
  noteContent.value = newContent
})

watch(() => props.initialTags, (newTags) => {
  noteTags.value = newTags.join(', ')
}, { deep: true })

/**
   * 保存笔记
   */
  const saveNote = async () => {
    isSaving.value = true
    try {
      // 检查是否所有内容都为空
      const isEmpty = !noteTitle.value.trim() && !noteContent.value.trim() && !noteTags.value.trim()
      
      if (isEmpty) {
        // 如果所有内容都为空且是编辑模式，则发送删除事件
        if (props.noteId) {
          emit('delete', props.noteId)
        }
        // 如果是新建模式，直接取消编辑
        else {
          emit('cancel')
        }
      } else {
        // 正常保存笔记
        const noteData = {
          title: noteTitle.value,
          content: noteContent.value,
          tags: noteTags.value.split(',').map(tag => tag.trim()).filter(tag => tag)
        }
        
        emit('save', noteData)
      }
    } catch (error) {
      console.error('保存笔记失败:', error)
    } finally {
      isSaving.value = false
    }
  }

/**
 * 取消编辑
 */
const cancelEdit = () => {
  emit('cancel')
}
</script>

<style scoped>
.note-editor {
  min-height: 700px;
}

.editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.editor-container:focus-within {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

:deep(.el-textarea__inner) {
  resize: none;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  font-size: 16px;
  line-height: 1.7;
}

:deep(.el-input__wrapper) {
  padding: 12px 16px;
  border-radius: 8px;
  transition: all 0.3s;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.el-button) {
  font-weight: 500;
  padding: 10px 24px;
}
</style>

