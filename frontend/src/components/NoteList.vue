<template>
  <div class="note-list" v-loading="loading">
    <el-table
      :data="list"
      style="width: 100%"
      v-if="list.length > 0"
      :scroll-y="400"
      height="400"
    >
      <el-table-column prop="title" label="标题" min-width="200">
        <template #default="{ row }">
          <span 
            class="note-title" 
            @click="handleNoteClick(row.id)"
          >
            {{ row.title }}
          </span>
        </template>
      </el-table-column>
      
      <el-table-column label="标签" min-width="200">
        <template #default="{ row }">
          <div class="tags-container">
            <el-tag
              v-for="(tag, index) in getVisibleTags(row.tags)"
              :key="index"
              size="small"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
            <el-tag
              v-if="getExtraTagsCount(row.tags) > 0"
              size="small"
              type="info"
              class="tag-item"
            >
              +{{ getExtraTagsCount(row.tags) }}
            </el-tag>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              type="primary"
              size="small"
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              type="warning"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 空状态 -->
    <el-empty v-else-if="!loading" description="暂无笔记数据" />

    <!-- 分页 -->
    <el-pagination
    v-if="total > 0"
    v-model="currentPage"
    :page-size="currentPageSize"
    @update:page-size="currentPageSize = $event"
    :total="total"
    :page-sizes="[10, 20, 50, 100]"
    layout="total, sizes, prev, pager, next, jumper"
    @current-change="handlePageChange"
    @size-change="handleSizeChange"
    class="pagination"
    />

  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// Props
const props = defineProps({
  page: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  },
  tags: {
    type: Array,
    default: () => []
  },
  list: {
    type: Array,
    default: () => []
  },
  total: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['page-change', 'note-click', 'view', 'edit', 'delete'])

// 内部状态
const currentPage = ref(props.page)
const currentPageSize = ref(props.pageSize)

// 监听 props 变化
watch(() => props.page, (newVal) => {
  currentPage.value = newVal
})

watch(() => props.pageSize, (newVal) => {
  currentPageSize.value = newVal
})

// 方法
const getVisibleTags = (tags) => {
  if (!tags || !Array.isArray(tags)) return []
  return tags.slice(0, 2)
}

const getExtraTagsCount = (tags) => {
  if (!tags || !Array.isArray(tags)) return 0
  return Math.max(0, tags.length - 2)
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleNoteClick = (noteId) => {
  emit('note-click', noteId)
}

const handlePageChange = (page) => {
  currentPage.value = page
  emit('page-change', {
    page,
    pageSize: currentPageSize.value,
    tags: props.tags
  })
}

const handleSizeChange = (size) => {
  currentPageSize.value = size
  currentPage.value = 1 // 重置到第一页
  emit('page-change', {
    page: 1,
    pageSize: size,
    tags: props.tags
  })
}

const handleView = (row) => {
  emit('view', row)
}

const handleEdit = (row) => {
  emit('edit', row)
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除笔记"${row.title}"吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    emit('delete', row)
  }).catch(() => {
    // 用户取消删除
  })
}
</script>

<style scoped>
.note-list {
  width: 100%;
}

.note-title {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
}

.note-title:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  margin: 2px 0;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.el-button-group {
  display: flex;
}

.el-button-group .el-button {
  margin-left: 0;
}
</style>