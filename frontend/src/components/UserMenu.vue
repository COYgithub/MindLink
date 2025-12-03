<!-- src/components/UserMenu.vue -->
<template>
  <div class="relative">
    <!-- 用户头像或用户名按钮 -->
    <button
      class="flex items-center space-x-2 px-3 py-2 rounded-lg transition-all hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium"
      @click="toggleMenu"
    >
      <div class="w-9 h-9 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white font-semibold shadow-md">
        {{ userNameInitials }}
      </div>
      <span>{{ userName || '用户' }}</span>
      <el-icon size="16" class="transition-transform duration-200" :class="{ 'rotate-180': isMenuOpen }">
        <ArrowDown />
      </el-icon>
    </button>

    <!-- 下拉菜单 -->
    <transition name="fade">
      <div
        v-if="isMenuOpen"
        class="absolute right-0 mt-2 w-56 rounded-xl shadow-xl py-1 z-50 overflow-hidden transition-all duration-300"
        :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }"
      >
        <router-link
          to="/settings"
          class="flex items-center space-x-3 block px-4 py-3 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          :class="{ 'text-gray-700': !isDarkMode, 'text-gray-300': isDarkMode }"
          @click="closeMenu"
        >
          <el-icon size="18" class="text-gray-500 dark:text-gray-400"><Setting /></el-icon>
          <span>设置</span>
        </router-link>
        <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>
        <button
          class="flex items-center space-x-3 block w-full text-left px-4 py-3 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          :class="{ 'text-gray-700': !isDarkMode, 'text-gray-300': isDarkMode }"
          @click="logout"
        >
          <el-icon size="18" class="text-gray-500 dark:text-gray-400"><SwitchButton /></el-icon>
          <span>登出</span>
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated, logout as authLogout } from '@/utils/auth'
import { ArrowDown, Setting, SwitchButton } from '@element-plus/icons-vue'
import { useDark } from '@/composables/useDark'

const router = useRouter()
const isMenuOpen = ref(false)
const userName = ref(localStorage.getItem('userName') || '用户') // 假设用户信息存储在 localStorage

// 使用深色模式组合式函数
const { isDarkMode } = useDark()

// 计算用户名首字母
const userNameInitials = computed(() => {
  if (!userName.value) return '用'
  return userName.value.charAt(0).toUpperCase()
})

// 切换菜单显示状态
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 关闭菜单
const closeMenu = () => {
  isMenuOpen.value = false
}

// 登出逻辑
const logout = () => {
  authLogout() // 调用 auth.js 中的登出方法
  router.push('/login') // 重定向到登录页面
  closeMenu()
}
</script>

<style scoped>
/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>