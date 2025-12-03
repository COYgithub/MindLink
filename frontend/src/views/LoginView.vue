<template>
  <div class="min-h-screen flex items-center justify-center transition-colors duration-300" :class="{ 'bg-gray-50': !isDarkMode, 'bg-gray-950': isDarkMode }">
    <div class="max-w-md w-full space-y-8 p-4">
      <div class="text-center">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">MindLink</h1>
        <p class="mt-3 text-lg opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-300': isDarkMode }">个人知识管理平台</p>
      </div>
      
      <div class="rounded-2xl shadow-xl overflow-hidden transition-all duration-500 hover:shadow-2xl scale-in" 
           :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }">
        <div class="p-8">
          <h2 class="text-2xl font-bold mb-8 text-center transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">登录</h2>
          
          <el-form
            :model="loginForm"
            :rules="loginRules"
            ref="loginFormRef"
            @submit.prevent="handleLogin"
            :validate-on-rule-change="false"
          >
            <el-form-item prop="username" class="mb-6">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                size="large"
                prefix-icon="User"
                class="rounded-xl transition-all duration-300 input-focus"
                :class="{ 
                  'bg-gray-50 border-gray-200 hover:border-blue-300 focus:border-blue-500': !isDarkMode, 
                  'bg-gray-700 border-gray-600 hover:border-blue-400 focus:border-blue-400 text-white': isDarkMode 
                }"
              />
            </el-form-item>
            
            <el-form-item prop="password" class="mb-6">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                prefix-icon="Lock"
                show-password
                class="rounded-xl transition-all duration-300 input-focus"
                :class="{ 
                  'bg-gray-50 border-gray-200 hover:border-blue-300 focus:border-blue-500': !isDarkMode, 
                  'bg-gray-700 border-gray-600 hover:border-blue-400 focus:border-blue-400 text-white': isDarkMode 
                }"
              />
            </el-form-item>
            
            <el-form-item class="mb-8">
              <div class="flex items-center justify-between">
                <el-checkbox v-model="loginForm.remember" :class="{ 'text-gray-700': !isDarkMode, 'text-gray-300': isDarkMode }">
                  记住我
                </el-checkbox>
                <el-link type="primary" :underline="false" class="hover:opacity-80 transition-opacity btn-hover">
                  忘记密码？
                </el-link>
              </div>
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="w-full rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:shadow-lg transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] btn-hover"
                :loading="isLoading"
                :disabled="!isFormValid"
                @click="handleLogin"
              >
                <span class="font-medium">登录</span>
              </el-button>
            </el-form-item>
          </el-form>
          
          <div class="text-center mt-8 pt-6 border-t transition-colors" :class="{ 'border-gray-200': !isDarkMode, 'border-gray-700': isDarkMode }">
            <span class="opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">还没有账号？</span>
            <el-link type="primary" :underline="false" @click="goToRegister" class="ml-1 hover:opacity-80 transition-opacity btn-hover">
              <span class="font-medium">立即注册</span>
            </el-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login as authLogin } from '@/utils/auth'
import { useDark } from '@/composables/useDark'

/**
 * 登录页面组件
 * 提供用户登录功能
 */

const router = useRouter()
const loginFormRef = ref()
const isLoading = ref(false)
const { isDarkMode } = useDark()

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

/**
 * 表单验证状态
 */
const isFormValid = computed(() => {
  return loginForm.username.trim() !== '' && loginForm.password.length >= 6
})

/**
 * 处理登录
 */
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    isLoading.value = true
    
    // 调用认证 API
    const response = await authLogin(loginForm.username, loginForm.password)
    
    ElMessage.success('登录成功，欢迎回来！')
    
    // 登录成功后跳转到首页
    router.push('/')
    
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.message || '登录失败，请检查用户名和密码是否正确')
  } finally {
    isLoading.value = false
  }
}

/**
 * 跳转到注册页面
 */
const goToRegister = () => {
  router.push('/register')
}
</script>
