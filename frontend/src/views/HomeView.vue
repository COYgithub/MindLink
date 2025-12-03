<!-- src/views/HomeView.vue -->
<template>
  <div class="min-h-screen transition-colors duration-300" :class="{ 'bg-gray-100': !isDarkMode, 'bg-gray-950': isDarkMode }">
    <!-- 导航栏 -->
    <nav class="shadow-md transition-colors duration-300" :class="{ 'bg-white': !isDarkMode, 'bg-gray-900': isDarkMode }">
      <div class="container mx-auto px-3 sm:px-4 py-3 sm:py-4 flex justify-between items-center">
        <h1 class="text-xl sm:text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">MindLink</h1>
        <div v-if="isAuthenticated()" class="flex items-center space-x-3 sm:space-x-6">
          <router-link to="/notes" class="text-sm sm:text-base text-gray-700 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors font-medium">
            我的笔记
          </router-link>
          <router-link to="/search" class="text-sm sm:text-base text-gray-700 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors font-medium">
            搜索
          </router-link>
          <UserMenu />
        </div>
        <div v-else class="flex items-center space-x-2 sm:space-x-4">
          <router-link to="/login" class="text-sm sm:text-base text-gray-700 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors font-medium">
            登录
          </router-link>
          <router-link to="/register" class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-3 sm:px-4 py-1 sm:py-2 rounded-lg hover:shadow-lg transition-all hover:-translate-y-0.5 font-medium">
            注册
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 页面内容 -->
    <div class="container mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-8 max-w-7xl mx-auto">
        <!-- 笔记管理卡片 -->
        <div class="rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:-translate-y-2 hover:shadow-xl cursor-pointer" 
             :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }" @click="$router.push('/notes')">
          <div class="p-6">
            <div class="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center mb-5 shadow-lg">
              <el-icon size="28" class="text-blue-600 dark:text-blue-400"><Document /></el-icon>
            </div>
            <h2 class="text-2xl font-bold mb-3 transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">笔记管理</h2>
            <p class="opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">
              创建、编辑和管理您的个人笔记，让灵感随时记录
            </p>
          </div>
          <div class="h-1 bg-gradient-to-r from-blue-500 to-blue-400"></div>
        </div>
        
        <!-- 知识图谱卡片 -->
        <div class="rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:-translate-y-2 hover:shadow-xl cursor-pointer" 
             :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }">
          <div class="p-6">
            <div class="w-14 h-14 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center mb-5 shadow-lg">
              <el-icon size="28" class="text-purple-600 dark:text-purple-400"><Connection /></el-icon>
            </div>
            <h2 class="text-2xl font-bold mb-3 transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">知识图谱</h2>
            <p class="opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">
              构建知识之间的关联关系，形成完整的知识网络
            </p>
          </div>
          <div class="h-1 bg-gradient-to-r from-purple-500 to-purple-400"></div>
        </div>
        
        <!-- 智能搜索卡片 -->
        <div class="rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:-translate-y-2 hover:shadow-xl cursor-pointer" 
             :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }" @click="$router.push('/search')">
          <div class="p-6">
            <div class="w-14 h-14 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center mb-5 shadow-lg">
              <el-icon size="28" class="text-green-600 dark:text-green-400"><Search /></el-icon>
            </div>
            <h2 class="text-2xl font-bold mb-3 transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">智能搜索</h2>
            <p class="opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">
              快速找到您需要的信息，支持全文检索和语义匹配
            </p>
          </div>
          <div class="h-1 bg-gradient-to-r from-green-500 to-green-400"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { isAuthenticated } from '@/utils/auth'
import UserMenu from '@/components/UserMenu.vue'
import { Document, Connection, Search } from '@element-plus/icons-vue'
import { useDark } from '@/composables/useDark'

// 使用深色模式组合式函数
const { isDarkMode } = useDark()
</script>
