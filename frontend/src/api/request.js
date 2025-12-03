import axios from 'axios'
import { ElMessage } from 'element-plus'
import { getToken, getTokenType } from '@/utils/auth'

/**
 * HTTP 请求封装
 * 统一处理请求和响应拦截
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// 创建 axios 实例
const request = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 请求拦截器
 * 在发送请求前添加认证 token
 */
request.interceptors.request.use(
  (config) => {
    // 从认证工具获取 token
    const token = getToken()
    const tokenType = getTokenType()
    if (token) {
      config.headers.Authorization = `${tokenType} ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 统一处理响应数据和错误
 */
request.interceptors.response.use(
  (response) => {
    const { data } = response
    
    // 如果后端返回的数据结构是 { code, data, message }
    if (data && typeof data === 'object' && 'code' in data) {
      if (data.code === 200) {
        return data.data
      } else {
        ElMessage.error(data.message || '请求失败')
        return Promise.reject(new Error(data.message || '请求失败'))
      }
    }
    
    // 直接返回数据
    return data
  },
  (error) => {
    const { response } = error
    
    if (response) {
      const { status, data } = response
      
      switch (status) {
        case 401:
          ElMessage.error('未授权，请重新登录')
          // 清除本地存储的 token
          import('@/utils/auth').then(({ removeToken }) => {
            removeToken()
          })
          // 跳转到登录页
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('拒绝访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data?.message || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default request
