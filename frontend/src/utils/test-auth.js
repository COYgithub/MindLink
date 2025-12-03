/**
 * 认证功能测试工具
 * 用于测试登录 API 是否正常工作
 */

import { login, isAuthenticated, getToken, removeToken } from './auth'

/**
 * 测试登录功能
 * @param {string} username - 测试用户名
 * @param {string} password - 测试密码
 */
export const testLogin = async (username = 'testuser', password = 'testpass123') => {
  console.log('🧪 开始测试登录功能...')
  
  try {
    // 清除之前的 token
    removeToken()
    console.log('✅ 已清除之前的认证信息')
    
    // 测试登录
    console.log(`📤 发送登录请求: ${username}`)
    const result = await login(username, password)
    console.log('✅ 登录成功:', result)
    
    // 验证 token 是否保存
    const token = getToken()
    const authenticated = isAuthenticated()
    console.log('🔑 Token:', token ? '已保存' : '未保存')
    console.log('🔐 认证状态:', authenticated ? '已认证' : '未认证')
    
    return {
      success: true,
      data: result,
      token,
      authenticated
    }
  } catch (error) {
    console.error('❌ 登录测试失败:', error.message)
    return {
      success: false,
      error: error.message
    }
  }
}

/**
 * 在浏览器控制台中运行测试
 * 使用方法：在浏览器控制台输入 testLogin()
 */
if (typeof window !== 'undefined') {
  window.testLogin = testLogin
  console.log('💡 提示：在控制台输入 testLogin() 来测试登录功能')
}

