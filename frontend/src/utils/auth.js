import axios from 'axios'
import { ElMessage } from 'element-plus'

/**
 * 认证相关工具函数
 * 处理用户登录、令牌管理等认证功能
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_KEY = 'access_token'
const TOKEN_TYPE_KEY = 'token_type'
const EXPIRES_AT_KEY = 'expires_at'

/**
 * 用户注册
 * 
 */
export const register = async (username, email, password, confirmPassword) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username,
      email,
      password,
      confirmPassword
    })

    const { code, data, message } = response.data

    if (code == 201) {
      return data
    } else {
      throw new Error(message || '注册失败')
    }
  } catch (error) {
    const { code, message } = response.data
    if (code == 400) {
      throw new Error('用户名已经被注册或者邮箱已经被注册')
    } else if (error.request) {
      throw new Error('网络错误')
    } else {
      throw new Error(message || '注册失败')
    }
  }

}

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise<Object>} 登录响应数据
 */
export const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, {
      username,
      password
    })
    
    const { code, data, message } = response.data
    
    if (code === 200) {
      // 保存令牌信息 - 从 data.tokens 中获取令牌信息
      setToken(data.tokens.access_token, data.tokens.token_type, Date.now() + data.tokens.expires_in * 1000)
      return data
    } else {
      throw new Error(message || '登录失败')
    }
  } catch (error) {
    if (error.response) {
      const { code, message } = error.response.data
      if (code === 401) {
        throw new Error('用户名或密码错误')
      } else {
        throw new Error(message || '登录失败')
      }
    } else if (error.request) {
      throw new Error('网络错误，请检查网络连接')
    } else {
      throw new Error(error.message || '登录失败')
    }
  }
}

/**
 * 用户登出
 */
export const logout = () => {
  removeToken()
  ElMessage.success('已退出登录')
}

/**
 * 设置认证令牌
 * @param {string} token - 访问令牌
 * @param {string} tokenType - 令牌类型
 * @param {number} expiresAt - 过期时间戳
 */
export const setToken = (token, tokenType = 'bearer', expiresAt) => {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(TOKEN_TYPE_KEY, tokenType)
  if (expiresAt) {
    localStorage.setItem(EXPIRES_AT_KEY, expiresAt.toString())
  }
}

/**
 * 获取访问令牌
 * @returns {string|null} 访问令牌
 */
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * 获取令牌类型
 * @returns {string} 令牌类型
 */
export const getTokenType = () => {
  return localStorage.getItem(TOKEN_TYPE_KEY) || 'bearer'
}

/**
 * 获取令牌过期时间
 * @returns {number|null} 过期时间戳
 */
export const getExpiresAt = () => {
  const expiresAt = localStorage.getItem(EXPIRES_AT_KEY)
  return expiresAt ? parseInt(expiresAt, 10) : null
}

/**
 * 移除所有令牌信息
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(TOKEN_TYPE_KEY)
  localStorage.removeItem(EXPIRES_AT_KEY)
}

/**
 * 检查令牌是否有效
 * @returns {boolean} 令牌是否有效
 */
export const isTokenValid = () => {
  const token = getToken()
  const expiresAt = getExpiresAt()
  
  if (!token) {
    return false
  }
  
  // 检查是否过期
  if (expiresAt && Date.now() >= expiresAt * 1000) {
    removeToken()
    return false
  }
  
  return true
}

/**
 * 获取认证头信息
 * @returns {Object} 认证头信息
 */
export const getAuthHeader = () => {
  const token = getToken()
  const tokenType = getTokenType()
  
  if (token) {
    return {
      'Authorization': `${tokenType} ${token}`
    }
  }
  
  return {}
}

/**
 * 检查用户是否已登录
 * @returns {boolean} 是否已登录
 */
export const isAuthenticated = () => {
  return isTokenValid()
}

