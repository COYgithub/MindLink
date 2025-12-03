import request from './request'

/**
 * 笔记相关 API 接口
 */

const NOTE_API_BASE = '/notes'

/**
 * 获取笔记列表
 * @param {Object} params - 查询参数
 * @returns {Promise} API 响应
 */
export const getNotes = (params = {}) => {
  return request.get(NOTE_API_BASE, { params })
}

/**
 * 获取单个笔记详情
 * @param {number} noteId - 笔记ID
 * @returns {Promise} API 响应
 */
export const getNoteById = (noteId) => {
  return request.get(`${NOTE_API_BASE}/${noteId}`)
}

/**
 * 创建新笔记
 * @param {Object} noteData - 笔记数据
 * @returns {Promise} API 响应
 */
export const createNote = (noteData) => {
  return request.post(NOTE_API_BASE, noteData)
}

/**
 * 更新笔记
 * @param {number} noteId - 笔记ID
 * @param {Object} noteData - 笔记数据
 * @returns {Promise} API 响应
 */
export const updateNote = (noteId, noteData) => {
  return request.put(`${NOTE_API_BASE}/${noteId}`, noteData)
}

/**
 * 更新笔记标签
 * @param {number} noteId - 笔记ID
 * @param {Object} noteTagData - 笔记标签数据
 * @returns {Promise} API 响应
 */
export const updateNoteTags = (noteId, noteTagData) => {
  return request.post(`${NOTE_API_BASE}/${noteId}/tags`, noteTagData)
}
/**
 * 删除笔记
 * @param {number} noteId - 笔记ID
 * @returns {Promise} API 响应
 */
export const deleteNote = (noteId) => {
  return request.delete(`${NOTE_API_BASE}/${noteId}`)
}

/**
 * 搜索笔记
 * @param {string} keyword - 搜索关键词
 * @param {Object} filters - 过滤条件
 * @returns {Promise} API 响应
 */
export const searchNotes = (keyword, filters = {}) => {
  return request.get(`${NOTE_API_BASE}/search`, {
    params: {
      q: keyword,
      ...filters
    }
  })
}

