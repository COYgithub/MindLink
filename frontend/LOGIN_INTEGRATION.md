# 登录功能集成说明

## 功能概述

已基于后端认证接口实现完整的登录功能，包括：

- ✅ 用户登录表单（Element Plus）
- ✅ 表单验证（用户名非空，密码长度≥6）
- ✅ 认证 API 集成
- ✅ Token 管理（localStorage）
- ✅ 路由守卫（未登录用户跳转登录页）
- ✅ 请求拦截器（自动添加认证头）

## 后端接口规范

### 登录接口
```
POST /api/v1/auth/login
Content-Type: application/json

请求体：
{
  "username": "string",
  "password": "string"
}

成功响应 (200)：
{
  "code": 200,
  "data": {
    "access_token": "string",
    "token_type": "bearer",
    "expires_at": 1234567890
  }
}

错误响应 (401)：
{
  "code": 401,
  "message": "用户名或密码错误"
}
```

## 文件结构

```
src/
├── utils/
│   ├── auth.js              # 认证工具函数
│   └── test-auth.js         # 登录功能测试工具
├── views/
│   └── LoginView.vue        # 登录页面组件
├── router/
│   └── index.js             # 路由配置（含认证守卫）
└── api/
    └── request.js           # HTTP 请求封装（含认证拦截器）
```

## 核心功能

### 1. 认证工具函数 (`src/utils/auth.js`)

```javascript
// 用户登录
const result = await login(username, password)

// 检查认证状态
const isAuth = isAuthenticated()

// 获取 Token
const token = getToken()

// 登出
logout()
```

### 2. 登录组件 (`src/views/LoginView.vue`)

- 使用 Element Plus 的 `ElForm` 组件
- 表单字段：`username`（用户名）、`password`（密码）
- 验证规则：用户名非空，密码长度≥6
- 提交按钮：加载状态 + 表单验证禁用
- 自动跳转：登录成功后跳转首页

### 3. 路由守卫 (`src/router/index.js`)

- 全局前置守卫检查 `meta.requiresAuth`
- 未登录用户自动跳转 `/login`
- 已登录用户访问登录页自动跳转首页

### 4. 请求拦截器 (`src/api/request.js`)

- 自动添加 `Authorization` 头
- 401 错误自动清除 Token 并跳转登录页
- 支持 Token 过期检查

## 环境配置

### 环境变量
```bash
# .env.local
VITE_API_URL=http://localhost:8000
```

### 后端服务要求
- 后端服务运行在 `http://localhost:8000`
- 提供 `/api/v1/auth/login` 接口
- 支持 CORS 跨域请求

## 测试方法

### 1. 浏览器控制台测试
```javascript
// 在浏览器控制台运行
testLogin('your_username', 'your_password')
```

### 2. 手动测试
1. 启动前端：`npm run dev`
2. 访问：http://localhost:3000
3. 点击登录，输入用户名密码
4. 检查是否成功跳转首页

### 3. 网络请求检查
- 打开浏览器开发者工具
- 查看 Network 标签
- 确认请求发送到正确的 API 端点
- 检查响应数据格式

## 错误处理

### 常见错误
1. **网络错误**：检查后端服务是否启动
2. **CORS 错误**：检查后端 CORS 配置
3. **401 错误**：用户名或密码错误
4. **Token 过期**：自动清除并跳转登录页

### 调试技巧
1. 查看浏览器控制台错误信息
2. 检查 Network 请求和响应
3. 使用 `testLogin()` 函数测试 API
4. 检查 localStorage 中的 Token 信息

## 安全注意事项

1. **Token 存储**：使用 localStorage 存储，注意 XSS 攻击
2. **HTTPS**：生产环境必须使用 HTTPS
3. **Token 过期**：定期刷新 Token 或重新登录
4. **敏感信息**：不要在客户端存储敏感信息

## 扩展功能

### 可添加的功能
- [ ] 记住我功能（延长 Token 有效期）
- [ ] 自动刷新 Token
- [ ] 多设备登录管理
- [ ] 登录日志记录
- [ ] 密码强度检查
- [ ] 验证码功能

### 相关文件
- `src/stores/userStore.js` - 用户状态管理
- `src/views/RegisterView.vue` - 注册页面
- `src/components/UserMenu.vue` - 用户菜单组件

