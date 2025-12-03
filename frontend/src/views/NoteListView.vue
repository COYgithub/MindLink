<template>
  <div class="note-list-view">
    <div class="page-header">
      <h2>笔记管理</h2>
      <el-button type="primary" @click="handleCreateNote">
        <el-icon><Plus /></el-icon>
        新建笔记
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-card shadow="never">
        <div class="filter-row">
          <div class="filter-item">
            <label>标签筛选：</label>
            <el-select
              v-model="selectedTags"
              multiple
              collapse-tags
              collapse-tags-tooltip
              placeholder="选择标签进行筛选"
              style="width: 300px"
              @change="handleTagsChange"
            >
              <el-option
                v-for="tag in allTags"
                :key="tag"
                :label="tag"
                :value="tag"
              />
            </el-select>
          </div>
          
          <div class="filter-actions">
            <el-button @click="handleClearFilters">清空筛选</el-button>
            <el-button type="primary" @click="handleRefresh">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 笔记列表组件 -->
    <div class="list-section">
      <el-card shadow="never">
        <NoteList
          :page="currentPage"
          :page-size="pageSize"
          :tags="selectedTags"
          :list="noteStore.list"
          :total="noteStore.total"
          :loading="noteStore.loading"
          @page-change="handlePageChange"
          @note-click="handleNoteClick"
          @view="handleViewNote"
          @edit="handleEditNote"
          @delete="handleDeleteNote"
        />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import NoteList from '@/components/NoteList.vue'
import { useNoteStore } from '@/stores/noteStore'

// 路由和状态管理
const router = useRouter()
const noteStore = useNoteStore()

// 响应式数据
const currentPage = ref(1)
const pageSize = ref(10)
const selectedTags = ref([])

// 计算属性
const allTags = computed(() => noteStore.allTags)

// 方法
const fetchNotes = async () => {
  try {
    await noteStore.fetchNotes(currentPage.value, pageSize.value, selectedTags.value)
  } catch (error) {
    ElMessage.error(error.message || '获取笔记列表失败')
  }
}

const handlePageChange = ({ page, pageSize: newPageSize, tags }) => {
  currentPage.value = page
  pageSize.value = newPageSize
  selectedTags.value = tags
  fetchNotes()
}

const handleTagsChange = () => {
  // 标签筛选变化时，重置到第一页
  currentPage.value = 1
  fetchNotes()
}

const handleClearFilters = () => {
  selectedTags.value = []
  currentPage.value = 1
  fetchNotes()
}

const handleRefresh = () => {
  fetchNotes()
}

const handleCreateNote = () => {
  router.push('/notes/new')
}

const handleNoteClick = (noteId) => {
  if (noteId) {
    router.push(`/notes/${noteId}`)
  }
}

const handleViewNote = (note) => {
  router.push(`/notes/${note.id}`)
}

const handleEditNote = (note) => {
  router.push(`/notes/${note.id}/edit`)
}

const handleDeleteNote = async (note) => {
  try {
    await noteStore.deleteNote(note.id)
    ElMessage.success('删除成功')
    
    // 如果当前页没有数据了，且不是第一页，则返回上一页
    if (noteStore.list.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }
    
    // 重新获取数据
    fetchNotes()
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
  }
}

// 生命周期
onMounted(() => {
  fetchNotes()
})
</script>

<style scoped>
.note-list-view {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  font-weight: 500;
  color: #606266;
  white-space: nowrap;
}

.filter-actions {
  display: flex;
  gap: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .note-list-view {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-item .el-select {
    width: 100% !important;
  }
  
  .filter-actions {
    justify-content: center;
  }
}
</style>