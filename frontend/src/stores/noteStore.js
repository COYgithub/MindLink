import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as noteApi from '@/api/noteApi'

/**
 * 笔记状态管理 Store
 * 管理笔记的增删改查操作
 */
export const useNoteStore = defineStore('note', () => {
  // 状态
  const notes = ref([])
  const currentNote = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // 计算属性
  const noteCount = computed(() => notes.value.length)
  const recentNotes = computed(() => 
    notes.value
      .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
      .slice(0, 5)
  )

  /**
   * 获取笔记列表
   * @param {Object} params - 查询参数
   */
  const fetchNotes = async (params = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await noteApi.getNotes(params)
      // 后端返回的是包含 items 和 pagination 的分页响应对象
      notes.value = data?.items || []
    } catch (err) {
      error.value = err.message
      console.error('获取笔记列表失败:', err)
    } finally {
      loading.value = false
    }
  }

  /**
 * 获取单个笔记详情
 * @param {number} noteId - 笔记ID
 */
const fetchNoteById = async (noteId) => {
  loading.value = true
  error.value = null
  
  try {
    // 检查 noteId 是否存在且有效
    if (!noteId) {
      throw new Error('无效的笔记ID')
    }
    
    const data = await noteApi.getNoteById(noteId)
    currentNote.value = data
    return data
  } catch (err) {
    error.value = err.message
    console.error('获取笔记详情失败:', err)
    throw err
  } finally {
    loading.value = false
  }
}

  /**
   * 创建新笔记
   * @param {Object} noteData - 笔记数据
   */
  const createNote = async (noteData) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await noteApi.createNote(noteData)
      notes.value.unshift(data)
      return data
    } catch (err) {
      error.value = err.message
      console.error('创建笔记失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新笔记
   * @param {number} noteId - 笔记ID
   * @param {Object} noteData - 笔记数据
   */
  const updateNote = async (noteId, noteData) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await noteApi.updateNote(noteId, noteData)
      const index = notes.value.findIndex(note => note.id === noteId)
      if (index !== -1) {
        notes.value[index] = data
      }
      if (currentNote.value && currentNote.value.id === noteId) {
        currentNote.value = data
      }
      return data
    } catch (err) {
      error.value = err.message
      console.error('更新笔记失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 删除笔记
   * @param {number} noteId - 笔记ID
   */
  const deleteNote = async (noteId) => {
    loading.value = true
    error.value = null
    
    try {
      await noteApi.deleteNote(noteId)
      const index = notes.value.findIndex(note => note.id === noteId)
      if (index !== -1) {
        notes.value.splice(index, 1)
      }
      if (currentNote.value && currentNote.value.id === noteId) {
        currentNote.value = null
      }
    } catch (err) {
      error.value = err.message
      console.error('删除笔记失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 搜索笔记
   * @param {string} keyword - 搜索关键词
   * @param {Object} filters - 过滤条件
   */
  const searchNotes = async (keyword, filters = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await noteApi.searchNotes(keyword, filters)
      return data || []
    } catch (err) {
      error.value = err.message
      console.error('搜索笔记失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 清空当前笔记
   */
  const clearCurrentNote = () => {
    currentNote.value = null
  }

  /**
   * 重置状态
   */
  const reset = () => {
    notes.value = []
    currentNote.value = null
    loading.value = false
    error.value = null
  }

  return {
    // 状态
    notes,
    currentNote,
    loading,
    error,
    
    // 计算属性
    noteCount,
    recentNotes,
    
    // 方法
    fetchNotes,
    fetchNoteById,
    createNote,
    updateNote,
    deleteNote,
    searchNotes,
    clearCurrentNote,
    reset
  }
})

