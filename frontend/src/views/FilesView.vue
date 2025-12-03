<template>
  <div class="files-container">
    <div class="files-header">
      <h1 class="text-2xl font-bold mb-2">文件管理</h1>
      <p class="text-gray-500 dark:text-gray-400 mb-4">上传和管理你的文件</p>
      
      <!-- 上传按钮 -->
      <el-button
        type="primary"
        :icon="Plus"
        class="mb-4"
        @click="handleUploadClick"
      >
        上传文件
      </el-button>
      
      <!-- 上传文件对话框 -->
      <el-dialog
        v-model="uploadDialogVisible"
        title="上传文件"
        width="500px"
      >
        <el-upload
          drag
          :action="apiBaseUrl + '/files/upload'"
          :headers="{ Authorization: authHeader }"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :auto-upload="false"
          ref="uploadRef"
          accept="*/*"
        >
          <el-icon class="el-icon--upload"><Upload /></el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip text-sm text-gray-500">
              支持多种文件格式，单个文件大小不超过 100MB
            </div>
          </template>
        </el-upload>
        
        <div class="mt-4">
          <el-form :model="uploadForm" label-width="80px">
            <el-form-item label="描述">
              <el-input
                v-model="uploadForm.description"
                placeholder="请输入文件描述"
                type="textarea"
                rows="2"
              />
            </el-form-item>
            
            <el-form-item label="是否公开">
              <el-switch v-model="uploadForm.isPublic" />
            </el-form-item>
          </el-form>
        </div>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="uploadDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitUpload">确定上传</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
    
    <!-- 文件列表 -->
    <el-card class="files-card">
      <el-table
        v-loading="loading"
        :data="filesList"
        stripe
        style="width: 100%"
        :scroll-y="400"
        height="400"
      >
        <el-table-column prop="filename" label="文件名" min-width="200">
          <template #default="scope">
            <div class="file-name">
              <el-icon class="mr-2"><Document /></el-icon>
              {{ scope.row.filename }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="file_size" label="文件大小" width="120">
          <template #default="scope">
            {{ formatFileSize(scope.row.file_size) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="file_type" label="文件类型" width="120" />
        
        <el-table-column prop="is_public" label="是否公开" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_public ? 'success' : 'info'">
              {{ scope.row.is_public ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="上传时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              :icon="Download"
              @click="handleDownload(scope.row.id)"
              class="mr-2"
            >
              下载
            </el-button>
            
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(scope.row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="mt-4 flex justify-center">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalFiles"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, Document, Download, Delete } from '@element-plus/icons-vue'
import axios from 'axios'
import { getAuthHeader } from '@/utils/auth'

// 上传文件对话框
const uploadDialogVisible = ref(false)
const uploadRef = ref(null)
const uploadForm = reactive({
  description: '',
  isPublic: false
})

// 文件列表数据
const filesList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalFiles = ref(0)

// API配置
const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// 认证头
const authHeader = computed(() => {
  const header = getAuthHeader()
  return header.Authorization || ''
})

// 获取文件列表
const fetchFilesList = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${apiBaseUrl}/files/`, {
      headers: getAuthHeader(),
      params: {
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value
      }
    })
    
    if (response.data.code === 200) {
      filesList.value = response.data.data.files || []
      totalFiles.value = response.data.data.total || 0
    } else {
      ElMessage.error('获取文件列表失败')
    }
  } catch (error) {
    console.error('获取文件列表失败:', error)
    ElMessage.error('获取文件列表失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

// 处理上传点击
const handleUploadClick = () => {
  uploadDialogVisible.value = true
}

// 提交上传
const submitUpload = () => {
  uploadRef.value.submit()
}

// 上传成功
const handleUploadSuccess = (response) => {
  if (response.code === 201) {
    ElMessage.success('文件上传成功')
    uploadDialogVisible.value = false
    uploadForm.description = ''
    uploadForm.isPublic = false
    fetchFilesList() // 重新获取文件列表
  } else {
    ElMessage.error('文件上传失败')
  }
}

// 上传失败
const handleUploadError = (error) => {
  console.error('文件上传失败:', error)
  ElMessage.error('文件上传失败，请重试')
}

// 处理下载
const handleDownload = async (fileId) => {
  try {
    // 使用 axios 发送带有认证头的请求
    const response = await axios.get(`${apiBaseUrl}/files/download/${fileId}`, {
      headers: getAuthHeader(),
      responseType: 'blob' // 重要：设置响应类型为 blob
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    
    // 从响应头获取文件名，如果没有则使用默认名称
    const contentDisposition = response.headers['content-disposition']
    let fileName = 'file-download'
    
    if (contentDisposition) {
      // 处理不同格式的Content-Disposition头
      const fileNameMatch = contentDisposition.match(/filename="(.+)"/i)
      if (fileNameMatch && fileNameMatch.length > 1) {
        fileName = fileNameMatch[1]
      } else {
        // 处理没有引号的情况
        const fileNameMatch2 = contentDisposition.match(/filename=([^;]+)/i)
        if (fileNameMatch2 && fileNameMatch2.length > 1) {
          fileName = fileNameMatch2[1].trim()
        }
      }
    } else {
      // 如果响应头中没有文件名，尝试从文件信息中获取
      // 先从文件列表中查找
      const fileInfo = filesList.value.find(f => f.id === fileId)
      if (fileInfo && fileInfo.filename) {
        fileName = fileInfo.filename
      } else {
        // 最后使用fileId作为默认名称
        fileName = `file-${fileId}`
      }
    }
    
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    
    // 触发下载
    link.click()
    
    // 清理
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('文件下载失败:', error)
    ElMessage.error('文件下载失败，请检查网络连接或权限')
  }
}

// 处理删除
const handleDelete = async (fileId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文件吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await axios.delete(`${apiBaseUrl}/files/${fileId}`, {
      headers: getAuthHeader()
    })
    
    if (response.data.code === 200) {
      ElMessage.success('文件删除成功')
      fetchFilesList() // 重新获取文件列表
    } else {
      ElMessage.error('文件删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('文件删除失败:', error)
      ElMessage.error('文件删除失败，请重试')
    }
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchFilesList()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchFilesList()
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(size) / Math.log(k))
  return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化日期时间
const formatDateTime = (dateTime) => {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 页面加载时获取文件列表
onMounted(() => {
  fetchFilesList()
})
</script>

<style scoped>
.files-container {
  padding: 20px;
}

.files-header {
  margin-bottom: 20px;
}

.file-name {
  display: flex;
  align-items: center;
}
</style>