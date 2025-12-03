<template>
  <div id="app" class="min-h-screen transition-colors duration-300" :class="{ 'dark': isDarkMode }">
    <el-container class="h-screen">
      <!-- 侧边栏 -->
      <el-aside
        :width="isSidebarCollapsed ? '70px' : '260px'"
        class="transition-all duration-300 shadow-lg border-r border-gray-200 dark:border-gray-700"
        :class="{ 'bg-white': !isDarkMode, 'bg-gray-900': isDarkMode }"
      >
        <div class="p-4 md:p-6 h-full flex flex-col">
          <!-- Logo -->
          <div class="flex items-center gap-3 mb-8 md:mb-10 justify-center md:justify-start">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
              <el-icon size="24" class="text-white"><Link /></el-icon>
            </div>
            <h1 v-if="!isSidebarCollapsed" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">MindLink</h1>
          </div>
          
          <!-- 导航菜单 -->
          <el-menu
            :default-active="$route.path"
            class="border-none bg-transparent flex-1"
            router
            active-text-color="#3b82f6"
            text-color="#6b7280"
            dark-text-color="#d1d5db"
            :dark="isDarkMode"
            :collapse="isSidebarCollapsed"
            :collapse-transition="true"
          >
            <el-menu-item index="/">
              <el-icon size="18" class="mr-2"><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/notes">
              <el-icon size="18" class="mr-2"><Document /></el-icon>
              <span>我的笔记</span>
            </el-menu-item>
            <el-menu-item index="/files">
              <el-icon size="18" class="mr-2"><UploadFilled /></el-icon>
              <span>文件管理</span>
            </el-menu-item>
            <el-menu-item index="/search">
              <el-icon size="18" class="mr-2"><Search /></el-icon>
              <span>搜索</span>
            </el-menu-item>
            <el-menu-item index="/settings">
              <el-icon size="18" class="mr-2"><Setting /></el-icon>
              <span>设置</span>
            </el-menu-item>
          </el-menu>
          
          <!-- 侧边栏控制 -->
          <div class="mt-auto pt-4 md:pt-8">
            <!-- 主题切换按钮 -->
            <div v-if="!isSidebarCollapsed" class="flex items-center justify-between p-3 rounded-lg bg-gray-100 dark:bg-gray-800 mb-4">
              <span class="text-sm text-gray-600 dark:text-gray-400">深色模式</span>
              <el-switch
                v-model="isDarkMode"
                size="small"
                inline-prompt
                active-text="开"
                inactive-text="关"
              />
            </div>
            
            <!-- 折叠/展开按钮 -->
            <div class="flex justify-center">
              <el-button
                type="default"
                circle
                :icon="isSidebarCollapsed ? 'el-icon-arrow-right' : 'el-icon-arrow-left'"
                class="transition-all duration-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                :class="{ 'w-10 h-10': true }"
                @click="toggleSidebar"
              />
            </div>
          </div>
        </div>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="p-0 md:p-6 bg-gray-50 dark:bg-gray-950 overflow-auto">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { House, Document, Search, Setting, Link, UploadFilled } from '@element-plus/icons-vue'
import { useDark } from '@/composables/useDark'

// 使用深色模式组合式函数
const { isDarkMode, toggleDarkMode } = useDark()

// 侧边栏折叠状态
const isSidebarCollapsed = ref(false)

// 切换侧边栏折叠状态
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
  // 保存状态到localStorage
  localStorage.setItem('sidebarCollapsed', isSidebarCollapsed.value)
}

// 响应式处理
const handleResize = () => {
  // 在小屏幕上自动折叠侧边栏
  if (window.innerWidth < 768) {
    isSidebarCollapsed.value = true
  } else {
    // 从localStorage恢复状态
    const savedState = localStorage.getItem('sidebarCollapsed')
    if (savedState !== null) {
      isSidebarCollapsed.value = savedState === 'true'
    } else {
      isSidebarCollapsed.value = false
    }
  }
}

// 组件挂载时
onMounted(() => {
  // 初始化状态
  handleResize()
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize)
})

// 组件卸载时
onUnmounted(() => {
  // 移除窗口大小变化监听
  window.removeEventListener('resize', handleResize)
})
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: all 0.3s ease;
}

/* 主题变量 */
:root {
  --primary-color: #3b82f6;
  --secondary-color: #8b5cf6;
  --bg-color: #f9fafb;
  --text-color: #111827;
  --sidebar-bg: #ffffff;
  --sidebar-text: #374151;
  --border-color: #e5e7eb;
}

.dark {
  --primary-color: #60a5fa;
  --secondary-color: #a78bfa;
  --bg-color: #111827;
  --text-color: #f9fafb;
  --sidebar-bg: #1f2937;
  --sidebar-text: #d1d5db;
  --border-color: #374151;
}

/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.dark ::-webkit-scrollbar-track {
  background: #374151;
}

.dark ::-webkit-scrollbar-thumb {
  background: #6b7280;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 卡片悬停动画 */
.card-hover {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 按钮动画 */
.btn-hover {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-hover:active {
  transform: translateY(1px);
}

/* 输入框聚焦动画 */
.input-focus {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-focus:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
}

/* 侧边栏过渡动画 */
.sidebar-transition {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 导航菜单动画 */
.menu-item {
  transition: all 0.2s ease;
}

.menu-item:hover {
  background-color: rgba(59, 130, 246, 0.1) !important;
}

/* 加载动画 */
.loading-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 缩放动画 */
.scale-in {
  animation: scaleIn 0.3s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* 滑动动画 */
.slide-up {
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Element Plus 菜单样式覆盖 */
.el-menu {
  --el-menu-bg-color: transparent;
  --el-menu-text-color: var(--sidebar-text);
  --el-menu-active-color: var(--primary-color);
  --el-menu-hover-bg-color: rgba(59, 130, 246, 0.1);
}

.dark .el-menu {
  --el-menu-text-color: var(--sidebar-text);
  --el-menu-hover-bg-color: rgba(96, 165, 250, 0.1);
}

.el-menu-item {
  --el-menu-item-font-size: 14px;
  --el-menu-item-height: 40px;
  border-radius: 8px;
  margin: 0 4px;
}

.el-menu-item.is-active {
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .el-aside {
    position: fixed !important;
    z-index: 100;
    height: 100vh;
    left: 0;
    top: 0;
    transition: left 0.3s ease;
  }
  
  .el-main {
    margin-left: 0 !important;
    transition: margin-left 0.3s ease;
  }
}

/* 移动端适配 */
@media (max-width: 480px) {
  .el-menu-item {
    --el-menu-item-height: 36px;
    font-size: 13px;
  }
  
  .el-button {
    font-size: 13px;
  }
}
</style>

