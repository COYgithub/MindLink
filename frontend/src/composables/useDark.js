// src/composables/useDark.js
import { ref, onMounted, watch } from 'vue'

export function useDark() {
  const isDarkMode = ref(false)

  // 初始化深色模式
  onMounted(() => {
    // 检查本地存储
    const savedTheme = localStorage.getItem('darkMode')
    if (savedTheme) {
      isDarkMode.value = savedTheme === 'true'
    } else {
      // 检查系统偏好
      isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    
    // 应用主题
    updateTheme()
  })

  // 监听isDarkMode变化，自动更新主题
  watch(isDarkMode, (newValue) => {
    updateTheme()
    localStorage.setItem('darkMode', newValue.toString())
  })

  // 切换深色模式
  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
  }

  // 更新主题
  const updateTheme = () => {
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    isDarkMode,
    toggleDarkMode
  }
}