<template>
  <div class="min-h-screen transition-colors duration-300" :class="{ 'bg-gray-50': !isDarkMode, 'bg-gray-950': isDarkMode }">
    <div class="container mx-auto px-3 sm:px-4 py-8 md:py-12 max-w-5xl">
      <div class="w-full">
        <h1 class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-8 sm:mb-10 text-center">搜索笔记</h1>
        
        <!-- 搜索框 -->
        <div class="mb-8 sm:mb-10">
          <el-input
            v-model="searchKeyword"
            placeholder="输入关键词搜索笔记..."
            size="large"
            @keyup.enter="handleSearch"
            @input="handleSearchInput"
            class="rounded-xl shadow-md w-full"
            :class="{ 
              'bg-white border-gray-200': !isDarkMode, 
              'bg-gray-800 border-gray-700': isDarkMode 
            }"
          >
            <template #prefix>
              <el-icon class="text-gray-500 dark:text-gray-400"><Search /></el-icon>
            </template>
            <template #append>
              <el-button 
                @click="handleSearch" 
                :loading="isSearching"
                class="bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:shadow-lg transition-all"
              >
                <span class="hidden sm:inline">搜索</span>
                <el-icon class="sm:hidden" size="18"><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>

        <!-- 搜索结果 -->
        <div v-if="searchResults.length > 0" class="space-y-6">
          <div class="text-sm font-medium opacity-80 transition-colors mb-6" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">
            找到 {{ searchResults.length }} 条结果
          </div>
          <div
            v-for="note in searchResults"
            :key="note.id"
            class="rounded-xl shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer overflow-hidden"
            :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }"
            @click="openNote(note.id)"
          >
            <div class="p-6">
              <h3 class="text-xl font-bold mb-3 transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">{{ note.title }}</h3>
              <p class="text-sm opacity-80 mb-5 line-clamp-3 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">{{ note.summary }}</p>
              <div class="flex flex-wrap gap-2 mb-4">
                <el-tag 
                  v-for="tag in note.tags || []" 
                  :key="tag"
                  size="small"
                  effect="plain"
                  class="rounded-full text-xs"
                  :class="{ 'bg-gray-100 text-gray-700': !isDarkMode, 'bg-gray-700 text-gray-300': isDarkMode }"
                >
                  {{ tag }}
                </el-tag>
                <el-tag 
                  v-if="(!note.tags || note.tags.length === 0)" 
                  size="small"
                  effect="plain"
                  class="rounded-full text-xs"
                  :class="{ 'bg-gray-100 text-gray-700': !isDarkMode, 'bg-gray-700 text-gray-300': isDarkMode }"
                >
                  无标签
                </el-tag>
              </div>
              <div class="flex justify-between items-center text-xs opacity-70">
                <span class="transition-colors" :class="{ 'text-gray-500': !isDarkMode, 'text-gray-400': isDarkMode }">{{ formatDate(note.updatedAt) }}</span>
                <div class="flex items-center space-x-2">
                  <el-icon size="14" class="transition-colors" :class="{ 'text-gray-500': !isDarkMode, 'text-gray-400': isDarkMode }">
                    <Calendar />
                  </el-icon>
                  <span class="transition-colors" :class="{ 'text-gray-500': !isDarkMode, 'text-gray-400': isDarkMode }">更新</span>
                </div>
              </div>
            </div>
            <!-- 装饰条 -->
            <div class="h-1 bg-gradient-to-r from-blue-500 to-purple-500"></div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="hasSearched && !isSearching" class="text-center py-16">
          <el-icon size="64" class="text-gray-400 mb-4"><Search /></el-icon>
          <p class="text-gray-500 dark:text-gray-400 text-lg">没有找到相关笔记</p>
          <p class="text-gray-500 dark:text-gray-500 text-sm mt-2">尝试使用其他关键词或检查拼写</p>
        </div>

        <!-- 加载状态 -->
        <div v-if="isSearching" class="text-center py-16">
          <el-icon size="40" class="text-blue-500 dark:text-blue-400 animate-spin mb-4"><Loading /></el-icon>
          <p class="text-gray-500 dark:text-gray-400 text-lg">搜索中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNoteStore } from '@/stores/noteStore'
import { debounce } from '@/utils/helpers'
import { formatDate } from '@/utils/helpers'
import { Search, Loading, Calendar } from '@element-plus/icons-vue'
import { useDark } from '@/composables/useDark'

/**
 * 搜索页面组件
 * 提供笔记搜索功能
 */

const router = useRouter()
const noteStore = useNoteStore()

// 使用深色模式组合式函数
const { isDarkMode } = useDark()

const searchKeyword = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const hasSearched = ref(false)

/**
 * 执行搜索
 */
const handleSearch = async () => {
  if (!searchKeyword.value.trim()) return
  
  isSearching.value = true
  hasSearched.value = true
  
  try {
    const results = await noteStore.searchNotes(searchKeyword.value)
    searchResults.value = results
  } catch (error) {
    console.error('搜索失败:', error)
    searchResults.value = []
  } finally {
    isSearching.value = false
  }
}

/**
 * 搜索输入处理（防抖）
 */
const handleSearchInput = debounce(() => {
  if (searchKeyword.value.trim()) {
    handleSearch()
  } else {
    searchResults.value = []
    hasSearched.value = false
  }
}, 500)

/**
 * 打开笔记
 * @param {number} noteId - 笔记ID
 */
const openNote = (noteId) => {
  if (noteId) {
    router.push(`/notes/${noteId}`)
  }
}

onMounted(() => {
  // 如果 URL 中有搜索参数，自动执行搜索
  const urlParams = new URLSearchParams(window.location.search)
  const q = urlParams.get('q')
  if (q) {
    searchKeyword.value = q
    handleSearch()
  }
})
</script>

