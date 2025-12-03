<template>
  <div class="min-h-screen transition-colors duration-300" :class="{ 'bg-gray-50': !isDarkMode, 'bg-gray-950': isDarkMode }">
    <div class="container mx-auto px-4 py-12">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-10 text-center">
          {{ isNewNote ? '创建新笔记' : '编辑笔记' }}
        </h1>
        <NoteEditor
          :note-id="noteId"
          :initial-title="note?.title || ''"
          :initial-content="note?.content || ''"
          :initial-tags="note?.tags || []"
          @save="handleSave"
          @cancel="handleCancel"
          @delete="handleDelete"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNoteStore } from '@/stores/noteStore'
import NoteEditor from '@/components/NoteEditor.vue'
import { useDark } from '@/composables/useDark'

/**
 * 笔记编辑页面组件
 * 提供笔记的创建和编辑功能
 */

const route = useRoute()
const router = useRouter()
const noteStore = useNoteStore()
const { isDarkMode } = useDark()

const note = ref(null)
const isNewNote = computed(() => route.name === 'NoteCreate')
const noteId = computed(() => isNewNote.value ? null : parseInt(route.params.id))

/**
 * 处理保存笔记
 * @param {Object} noteData - 笔记数据
 */
const handleSave = async (noteData) => {
  try {
    if (isNewNote.value) {
      await noteStore.createNote(noteData)
    } else {
      await noteStore.updateNote(noteId.value, noteData)
    }
    
    // 保存成功后跳转到笔记列表
    router.push('/notes')
  } catch (error) {
    console.error('保存笔记失败:', error)
  }
}

/**
   * 处理取消编辑
   */
  const handleCancel = () => {
    router.push('/notes')
  }

  /**
   * 处理删除笔记
   * @param {number} noteId - 笔记ID
   */
  const handleDelete = async (noteId) => {
    try {
      await noteStore.deleteNote(noteId)
      router.push('/notes')
    } catch (error) {
      console.error('删除笔记失败:', error)
    }
  }

onMounted(async () => {
  if (!isNewNote.value && noteId.value) {
    try {
      note.value = await noteStore.fetchNoteById(noteId.value)
    } catch (error) {
      console.error('获取笔记详情失败:', error)
      router.push('/notes')
    }
  }
})
</script>

