# MindLink 前端项目

基于 Vue 3 + Element Plus + Tailwind CSS 的个人知识管理平台前端应用。

## 技术栈

- **框架**: Vue 3.3+ (Composition API + `<script setup>`)
- **路由**: Vue Router 4.2+
- **状态管理**: Pinia 2.1+
- **UI 组件库**: Element Plus 2.4+
- **样式**: Tailwind CSS v3
- **构建工具**: Vite 5.0+
- **代码规范**: ESLint + Prettier

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API 接口
│   │   ├── request.js     # HTTP 请求封装
│   │   └── noteApi.js     # 笔记相关 API
│   ├── components/        # 公共组件
│   │   └── NoteEditor.vue # 笔记编辑器
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── stores/            # Pinia 状态管理
│   │   ├── index.js       # Store 入口
│   │   ├── noteStore.js   # 笔记状态管理
│   │   └── userStore.js   # 用户状态管理
│   ├── utils/             # 工具函数
│   │   ├── constants.js   # 常量定义
│   │   └── helpers.js     # 辅助函数
│   ├── views/             # 页面组件
│   │   ├── HomeView.vue   # 首页
│   │   ├── NotesView.vue  # 笔记列表
│   │   ├── NoteEditorView.vue # 笔记编辑
│   │   ├── SearchView.vue # 搜索页面
│   │   ├── SettingsView.vue # 设置页面
│   │   ├── LoginView.vue  # 登录页面
│   │   ├── RegisterView.vue # 注册页面
│   │   └── NotFoundView.vue # 404 页面
│   ├── App.vue            # 根组件
│   ├── main.js            # 应用入口
│   └── style.css          # 全局样式
├── index.html             # HTML 模板
├── package.json           # 项目配置
├── vite.config.js         # Vite 配置
├── tailwind.config.js     # Tailwind 配置
├── postcss.config.js      # PostCSS 配置
├── .eslintrc.js           # ESLint 配置
├── .prettierrc            # Prettier 配置
└── env.example            # 环境变量示例
```

## 开发指南

### 环境要求

- Node.js >= 18.0.0
- npm >= 8.0.0 或 yarn >= 1.22.0

### 安装依赖

```bash
cd frontend
npm install
```

### 开发环境

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
# ESLint 检查
npm run lint

# Prettier 格式化
npm run format
```

## 代码规范

### 文件命名

- **组件文件**: PascalCase (如 `NoteEditor.vue`)
- **工具文件**: camelCase (如 `helpers.js`)
- **常量文件**: camelCase (如 `constants.js`)

### 变量命名

- **函数/变量**: camelCase (如 `userName`, `handleClick`)
- **常量**: UPPER_SNAKE_CASE (如 `API_ENDPOINTS`)
- **组件名**: PascalCase (如 `NoteEditor`)

### 注释规范

关键逻辑必须添加文档注释：

```javascript
/**
 * 创建新笔记
 * @param {Object} noteData - 笔记数据
 * @returns {Promise} API 响应
 */
const createNote = async (noteData) => {
  // 实现逻辑
}
```

## 功能特性

### 已实现功能

- ✅ 响应式布局设计
- ✅ 路由导航和权限控制
- ✅ 用户认证状态管理
- ✅ 笔记 CRUD 操作
- ✅ 搜索功能
- ✅ 设置页面
- ✅ 404 错误页面

### 待实现功能

- ⏳ 笔记标签管理
- ⏳ 文件上传功能
- ⏳ 笔记分享功能
- ⏳ 主题切换
- ⏳ 国际化支持

## API 集成

前端通过 `/api` 路径代理到后端服务 (http://localhost:8000)。

### 环境变量配置

复制 `env.example` 为 `.env.local` 并配置：

```bash
# API 基础地址
VITE_API_BASE_URL=http://localhost:8000
```

## 部署说明

### 开发环境

1. 确保后端服务运行在 http://localhost:8000
2. 启动前端开发服务器：`npm run dev`
3. 访问 http://localhost:3000

### 生产环境

1. 构建项目：`npm run build`
2. 将 `dist` 目录部署到 Web 服务器
3. 配置 Nginx 代理 API 请求到后端服务

## 浏览器支持

- Chrome >= 88
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 许可证

MIT License

