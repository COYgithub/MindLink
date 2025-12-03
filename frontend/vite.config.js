import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { resolve } from 'path'
// 改为 ESM 导入方式
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

/**
 * Vite 配置文件
 * 配置 Vue 3 + Element Plus + Tailwind CSS
 */
export default defineConfig({
  plugins: [
    vue(),
    // 自动导入 Vue API
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia'],
      dts: true,
      resolvers: [ElementPlusResolver()]
    }),
    // 自动导入组件
    Components({
      resolvers: [ElementPlusResolver()],
      dts: true
    })
  ],
  
  // 路径别名
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  
  // 开发服务器配置
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  
  // 构建配置
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue'],
          'vue-router': ['vue-router'],
          pinia: ['pinia'],
          'element-plus': ['element-plus'],
          'element-plus-icons': ['@element-plus/icons-vue']
        }
      }
    }
  },
  
  // CSS 预处理器配置（已修复）
  css: {
    postcss: {
      plugins: [
        tailwindcss,  // 直接使用导入的变量
        autoprefixer
      ]
    }
  },
  
  // 环境变量前缀
  envPrefix: 'VITE_'
})
    
