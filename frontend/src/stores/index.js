import { createPinia } from 'pinia'

/**
 * Pinia Store 配置
 * 导出 Pinia 实例和所有 Store
 */

export { createPinia }

// 导出所有 Store
export { useNoteStore } from './noteStore'
export { useUserStore } from './userStore'

