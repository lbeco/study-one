import { defineStore } from 'pinia'
import tagService from '../services/tag'

// 标签状态管理
export const useTagStore = defineStore('tag', {
  state: () => ({
    tags: [],
    currentTag: null,
    loading: false,
    error: null
  }),

  getters: {
    getTagById: (state) => (id) => {
      return state.tags.find(tag => tag.id === id)
    }
  },

  actions: {
    // 获取标签列表
    async fetchTags(params) {
      this.loading = true
      this.error = null
      try {
        const response = await tagService.getTags(params)
        this.tags = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取标签列表失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 获取单个标签
    async fetchTag(id) {
      this.loading = true
      this.error = null
      try {
        const response = await tagService.getTag(id)
        this.currentTag = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取标签失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 创建标签
    async createTag(data) {
      this.loading = true
      this.error = null
      try {
        const response = await tagService.createTag(data)
        this.tags.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('创建标签失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新标签
    async updateTag(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await tagService.updateTag(id, data)
        const index = this.tags.findIndex(tag => tag.id === id)
        if (index !== -1) {
          this.tags[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('更新标签失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 删除标签
    async deleteTag(id) {
      this.loading = true
      this.error = null
      try {
        await tagService.deleteTag(id)
        this.tags = this.tags.filter(tag => tag.id !== id)
      } catch (error) {
        this.error = error.message
        console.error('删除标签失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
