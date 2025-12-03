/**
 * 应用常量定义
 */

// API 相关常量
export const API_ENDPOINTS = {
  NOTES: '/api/notes',
  USERS: '/api/users',
  AUTH: '/api/auth'
}

// 本地存储键名
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info'
}

// 路由名称
export const ROUTE_NAMES = {
  HOME: 'Home',
  NOTES: 'Notes',
  NOTE_EDITOR: 'NoteEditor',
  LOGIN: 'Login',
  REGISTER: 'Register'
}

// 笔记状态
export const NOTE_STATUS = {
  DRAFT: 'draft',
  PUBLISHED: 'published',
  ARCHIVED: 'archived'
}

// 分页配置
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  MAX_PAGE_SIZE: 100
}

// 文件上传配置
export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'text/plain', 'application/pdf']
}

// 日期时间格式
export const DATE_FORMATS = {
  DATE: 'YYYY-MM-DD',
  DATETIME: 'YYYY-MM-DD HH:mm:ss',
  TIME: 'HH:mm:ss'
}

