import { createRouter, createWebHistory } from 'vue-router'
import { ROUTE_NAMES } from '@/utils/constants'
import { isAuthenticated } from '@/utils/auth'

/**
 * 路由配置
 * 定义应用的所有路由规则
 */

const routes = [
  {
    path: '/',
    name: ROUTE_NAMES.HOME,
    component: () => import('@/views/HomeView.vue'),
    meta: {
      title: '首页',
      requiresAuth: false
    }
  },
  {
    path: '/notes',
    name: ROUTE_NAMES.NOTES,
    component: () => import('@/views/NotesView.vue'),
    meta: {
      title: '我的笔记',
      requiresAuth: true
    }
  },
  {    path: '/notes/list',    name: 'NoteList',    component: () => import('@/views/NoteListView.vue'),    meta: {      title: '笔记列表',      requiresAuth: true    }  },
  {
    path: '/notes/:id',
    name: ROUTE_NAMES.NOTE_EDITOR,
    component: () => import('@/views/NoteEditorView.vue'),
    meta: {
      title: '编辑笔记',
      requiresAuth: true
    }
  },
  {
    path: '/notes/new',
    name: 'NoteCreate',
    component: () => import('@/views/NoteEditorView.vue'),
    meta: {
      title: '新建笔记',
      requiresAuth: true
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/SearchView.vue'),
    meta: {
      title: '搜索',
      requiresAuth: false
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: {
      title: '设置',
      requiresAuth: true
    }
  },
  {
    path: '/files',
    name: 'Files',
    component: () => import('@/views/FilesView.vue'),
    meta: {
      title: '文件管理',
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: ROUTE_NAMES.LOGIN,
    component: () => import('@/views/LoginView.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/register',
    name: ROUTE_NAMES.REGISTER,
    component: () => import('@/views/RegisterView.vue'),
    meta: {
      title: '注册',
      requiresAuth: false
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: {
      title: '页面未找到',
      requiresAuth: false
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

/**
 * 路由守卫
 * 处理认证和页面标题
 */
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - MindLink`
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      // 未登录用户跳转到登录页
      next('/login')
      return
    }
  }

  // 如果已登录用户访问登录页，重定向到首页
  if (to.path === '/login' && isAuthenticated()) {
    next('/')
    return
  }

  next()
})

export default router
