<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">设置</h1>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- 设置菜单 -->
          <div class="lg:col-span-1">
            <div class="bg-white rounded-lg shadow-md p-6">
              <h2 class="text-lg font-semibold text-gray-800 mb-4">设置选项</h2>
              <el-menu
                :default-active="activeTab"
                class="border-none"
                @select="handleTabChange"
              >
                <el-menu-item index="profile">
                  <el-icon><User /></el-icon>
                  <span>个人资料</span>
                </el-menu-item>
                <el-menu-item index="account">
                  <el-icon><Key /></el-icon>
                  <span>账户安全</span>
                </el-menu-item>
                <el-menu-item index="preferences">
                  <el-icon><Setting /></el-icon>
                  <span>偏好设置</span>
                </el-menu-item>
                <el-menu-item index="about">
                  <el-icon><InfoFilled /></el-icon>
                  <span>关于</span>
                </el-menu-item>
              </el-menu>
            </div>
          </div>

          <!-- 设置内容 -->
          <div class="lg:col-span-2">
            <div class="bg-white rounded-lg shadow-md p-6">
              <!-- 个人资料 -->
              <div v-if="activeTab === 'profile'" class="space-y-6">
                <h3 class="text-xl font-semibold text-gray-800">个人资料</h3>
                <el-form :model="profileForm" label-width="100px">
                  <el-form-item label="用户名">
                    <el-input v-model="profileForm.username" />
                  </el-form-item>
                  <el-form-item label="邮箱">
                    <el-input v-model="profileForm.email" />
                  </el-form-item>
                  <el-form-item label="昵称">
                    <el-input v-model="profileForm.nickname" />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="updateProfile">保存</el-button>
                  </el-form-item>
                </el-form>
              </div>

              <!-- 账户安全 -->
              <div v-if="activeTab === 'account'" class="space-y-6">
                <h3 class="text-xl font-semibold text-gray-800">账户安全</h3>
                <el-form :model="passwordForm" label-width="100px">
                  <el-form-item label="当前密码">
                    <el-input v-model="passwordForm.currentPassword" type="password" show-password />
                  </el-form-item>
                  <el-form-item label="新密码">
                    <el-input v-model="passwordForm.newPassword" type="password" show-password />
                  </el-form-item>
                  <el-form-item label="确认密码">
                    <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="updatePassword">修改密码</el-button>
                  </el-form-item>
                </el-form>
              </div>

              <!-- 偏好设置 -->
              <div v-if="activeTab === 'preferences'" class="space-y-6">
                <h3 class="text-xl font-semibold text-gray-800">偏好设置</h3>
                <el-form label-width="120px">
                  <el-form-item label="主题模式">
                    <el-radio-group v-model="preferences.theme">
                      <el-radio label="light">浅色</el-radio>
                      <el-radio label="dark">深色</el-radio>
                      <el-radio label="auto">跟随系统</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item label="语言">
                    <el-select v-model="preferences.language" style="width: 200px">
                      <el-option label="简体中文" value="zh-CN" />
                      <el-option label="English" value="en-US" />
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="updatePreferences">保存设置</el-button>
                  </el-form-item>
                </el-form>
              </div>

              <!-- 关于 -->
              <div v-if="activeTab === 'about'" class="space-y-6">
                <h3 class="text-xl font-semibold text-gray-800">关于 MindLink</h3>
                <div class="space-y-4">
                  <p class="text-gray-600">版本: 1.0.0</p>
                  <p class="text-gray-600">基于 Vue 3 + Element Plus 构建</p>
                  <p class="text-gray-600">个人知识管理平台</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { User, Key, Setting, InfoFilled } from '@element-plus/icons-vue'

/**
 * 设置页面组件
 * 提供用户设置和偏好配置功能
 */

const activeTab = ref('profile')

const profileForm = reactive({
  username: '',
  email: '',
  nickname: ''
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const preferences = reactive({
  theme: 'light',
  language: 'zh-CN'
})

/**
 * 切换设置标签页
 * @param {string} tab - 标签页名称
 */
const handleTabChange = (tab) => {
  activeTab.value = tab
}

/**
 * 更新个人资料
 */
const updateProfile = () => {
  // TODO: 实现更新个人资料逻辑
  console.log('更新个人资料:', profileForm)
}

/**
 * 修改密码
 */
const updatePassword = () => {
  // TODO: 实现修改密码逻辑
  console.log('修改密码:', passwordForm)
}

/**
 * 更新偏好设置
 */
const updatePreferences = () => {
  // TODO: 实现更新偏好设置逻辑
  console.log('更新偏好设置:', preferences)
}
</script>

