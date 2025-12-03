<template>
  <div class="min-h-screen transition-colors duration-300 scale-in" :class="{ 'bg-gray-50': !isDarkMode, 'bg-gray-950': isDarkMode }">
    <div class="container mx-auto px-3 sm:px-4 py-6 md:py-10 max-w-7xl">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 md:mb-10 gap-4">
        <h1 class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">我的笔记</h1>
        <el-button type="primary" @click="createNote" :icon="Plus" class="w-full sm:w-auto bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:shadow-lg hover:-translate-y-0.5 btn-hover">
          新建笔记
        </el-button>
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6 md:gap-8">
        <div 
          v-for="(note, index) in notes" 
          :key="note.id"
          class="rounded-xl shadow-md cursor-pointer overflow-hidden card-hover relative"
          :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }"
          @click="openNote(note.id)"
          style="animation-delay: calc(0.05s * var(--index))"
          :style="{ '--index': index }"
        >
          <!-- 删除按钮 -->
          <div class="absolute top-3 right-3 z-10">
            <el-button
              size="small"
              circle
              type="danger"
              @click.stop="deleteNote(note.id)"
              :class="{ 'bg-red-500 hover:bg-red-600 border-0': !isDarkMode, 'bg-red-600 hover:bg-red-700 border-0': isDarkMode }"
              title="删除笔记"
            >
              <el-icon size="16"><Delete /></el-icon>
            </el-button>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold mb-3 transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">{{ note.title }}</h3>
            <p class="text-sm opacity-80 mb-5 line-clamp-3 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">{{ note.summary }}</p>
            <div class="flex flex-wrap gap-2 mb-4">
              <el-tag 
                v-for="tag in note.tags || []" 
                :key="tag"
                size="small"
                effect="plain"
                class="rounded-full text-xs transition-all hover:scale-105 hover:shadow-md"
                :class="{ 'bg-gray-100 text-gray-700': !isDarkMode, 'bg-gray-700 text-gray-300': isDarkMode }"
              >
                {{ tag }}
              </el-tag>
              <el-tag 
                v-if="(!note.tags || note.tags.length === 0)" 
                size="small"
                effect="plain"
                class="rounded-full text-xs transition-all hover:scale-105 hover:shadow-md"
                :class="{ 'bg-gray-100 text-gray-700': !isDarkMode, 'bg-gray-700 text-gray-300': isDarkMode }"
              >
                无标签
              </el-tag>
            </div>
            <div class="flex justify-between items-center text-xs opacity-70">
              <span class="transition-colors" :class="{ 'text-gray-500': !isDarkMode, 'text-gray-400': isDarkMode }">{{ formatDate(note.updatedAt) }}</span>
              <div class="flex items-center space-x-2">
                <el-icon size="14" class="transition-colors hover:text-blue-500 dark:hover:text-blue-400 duration-300"><Calendar /></el-icon>
                <span class="transition-colors" :class="{ 'text-gray-500': !isDarkMode, 'text-gray-400': isDarkMode }">更新</span>
              </div>
            </div>
          </div>
          <!-- 装饰条 -->
          <div class="h-1 bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Calendar, Delete } from '@element-plus/icons-vue'
import { useNoteStore } from '@/stores/noteStore'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import { useDark } from '@/composables/useDark'
import { ElMessage } from 'element-plus'

/**
 * 笔记列表页面组件
 * 展示用户的所有笔记，支持创建和查看
 */
// 路由和状态管理
const router = useRouter()
const noteStore = useNoteStore()
const notes = ref([])
const loading = ref(true)

// 使用深色模式组合式函数
const { isDarkMode } = useDark()

/**
 * 创建新笔记
 */
const createNote = () => {
  router.push(`/notes/new`)
  console.log('创建新笔记')
}

/**
 * 打开指定笔记
 * @param {number} noteId - 笔记ID
 */
const openNote = (noteId) => {
  if (noteId) {
    router.push(`/notes/${noteId}`)
    console.log('打开笔记:', noteId)
  }
}

const deleteNote = async (noteId) => {
  try {
    await noteStore.deleteNote(noteId)
    // 从本地列表中移除删除的笔记
    notes.value = notes.value.filter(note => note.id !== noteId)
    ElMessage.success('笔记删除成功')
  } catch (error) {
    console.error('删除笔记失败:', error)
    ElMessage.error('删除笔记失败，请重试')
  }
}

/**
 * 格式化日期
 * @param {string} date - 日期字符串
 * @returns {string} 格式化后的日期
 */
const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

onMounted(async () => {
  await noteStore.fetchNotes()
  notes.value = noteStore.notes
})
</script>