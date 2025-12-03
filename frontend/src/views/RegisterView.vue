<template>
  <div class="min-h-screen flex items-center justify-center transition-colors duration-300 scale-in" :class="{ 'bg-gray-50': !isDarkMode, 'bg-gray-950': isDarkMode }">
    <div class="max-w-md w-full space-y-8 p-4">
      <div class="text-center">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">MindLink</h1>
        <p class="mt-3 text-lg opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-300': isDarkMode }">连接思想，创造无限可能</p>
      </div>
      
      <div class="rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300" :class="{ 'bg-white': !isDarkMode, 'bg-gray-800': isDarkMode }">
        <div class="p-8">
          <h2 class="text-2xl font-bold mb-8 text-center transition-colors" :class="{ 'text-gray-800': !isDarkMode, 'text-white': isDarkMode }">注册</h2>
          
          <el-form
            :model="registerForm"
            :rules="registerRules"
            ref="registerFormRef"
            @submit.prevent="handleRegister"
            :validate-on-rule-change="false"
          >
            <el-form-item prop="username" class="mb-5">
              <el-input
                v-model="registerForm.username"
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
            
            <el-form-item prop="email" class="mb-5">
              <el-input
                v-model="registerForm.email"
                placeholder="请输入邮箱"
                size="large"
                prefix-icon="Message"
                class="rounded-xl transition-all duration-300 input-focus"
                :class="{ 
                  'bg-gray-50 border-gray-200 hover:border-blue-300 focus:border-blue-500': !isDarkMode, 
                  'bg-gray-700 border-gray-600 hover:border-blue-400 focus:border-blue-400 text-white': isDarkMode 
                }"
              />
            </el-form-item>
            
            <el-form-item prop="password" class="mb-5">
              <el-input
                v-model="registerForm.password"
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
            
            <el-form-item prop="confirmPassword" class="mb-7">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请确认密码"
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
              <el-checkbox v-model="registerForm.agree" :class="{ 'text-gray-700': !isDarkMode, 'text-gray-300': isDarkMode }">
                我已阅读并同意
                <el-link type="primary" :underline="false" class="btn-hover">《用户协议》</el-link>
                和
                <el-link type="primary" :underline="false" class="btn-hover">《隐私政策》</el-link>
              </el-checkbox>
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="w-full rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:shadow-lg transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] btn-hover"
                :loading="isLoading"
                @click="handleRegister"
              >
                <span class="font-medium">注册</span>
              </el-button>
            </el-form-item>
          </el-form>
          
          <div class="text-center mt-8 pt-6 border-t transition-colors" :class="{ 'border-gray-200': !isDarkMode, 'border-gray-700': isDarkMode }">
            <span class="opacity-80 transition-colors" :class="{ 'text-gray-600': !isDarkMode, 'text-gray-400': isDarkMode }">已有账号？</span>
            <el-link type="primary" :underline="false" @click="goToLogin" class="ml-1 hover:opacity-80 transition-opacity btn-hover">
              <span class="font-medium">立即登录</span>
            </el-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { validatePassword } from '@/utils/helpers'
import { register as authRegister } from '@/utils/auth'
import { useDark } from '@/composables/useDark'
/**
 * 注册页面组件
 * 提供用户注册功能
 */

const router = useRouter()
const registerFormRef = ref()
const isLoading = ref(false)
const { isDarkMode } = useDark()

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agree: false
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        const validation = validatePassword(value)
        if (!validation.isValid) {
          callback(new Error('密码强度不够，请包含大小写字母、数字和特殊字符'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

/**
 * 处理注册
 */
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return
    
    if (!registerForm.agree) {
      ElMessage.warning('请先同意用户协议和隐私政策')
      return
    }
    
    isLoading.value = true
    
    const response = await authRegister(registerForm.username, registerForm.email, registerForm.password, registerForm.confirmPassword)
    
    // 注册成功
    setTimeout(() => {
      ElMessage.success('注册成功！欢迎加入MindLink')
      router.push('/login')
      isLoading.value = false
    }, 1000)
    
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error(error.message || '注册失败，请检查输入信息并重试')
    isLoading.value = false
  }
}

/**
 * 跳转到登录页面
 */
const goToLogin = () => {
  router.push('/login')
}
</script>

