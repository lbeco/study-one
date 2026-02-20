import { defineStore } from 'pinia'
import knowledgeService from '../services/knowledge'

// 知识项状态管理
export const useKnowledgeStore = defineStore('knowledge', {
  state: () => ({
    knowledgeItems: [],
    currentKnowledgeItem: null,
    markdownContent: null,
    webpageContent: null,
    fetchedWebpageContent: null,
    loading: false,
    error: null
  }),

  getters: {
    getKnowledgeItemById: (state) => (id) => {
      return state.knowledgeItems.find(item => item.id === id)
    }
  },

  actions: {
    // 获取知识项列表
    async fetchKnowledgeItems(params) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.getKnowledgeItems(params)
        this.knowledgeItems = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取知识项列表失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 搜索知识项
    async searchKnowledge(params) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.searchKnowledge(params)
        this.knowledgeItems = response.data
      } catch (error) {
        this.error = error.message
        console.error('搜索知识项失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 按标签查询知识项
    async fetchKnowledgeByTags(params) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.getKnowledgeByTags(params)
        this.knowledgeItems = response.data
      } catch (error) {
        this.error = error.message
        console.error('按标签查询知识项失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 获取单个知识项
    async fetchKnowledgeItem(id) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.getKnowledgeItem(id)
        this.currentKnowledgeItem = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取知识项失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 创建知识项
    async createKnowledgeItem(data) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.createKnowledgeItem(data)
        this.knowledgeItems.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('创建知识项失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新知识项
    async updateKnowledgeItem(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.updateKnowledgeItem(id, data)
        const index = this.knowledgeItems.findIndex(item => item.id === id)
        if (index !== -1) {
          this.knowledgeItems[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('更新知识项失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 删除知识项
    async deleteKnowledgeItem(id) {
      this.loading = true
      this.error = null
      try {
        await knowledgeService.deleteKnowledgeItem(id)
        this.knowledgeItems = this.knowledgeItems.filter(item => item.id !== id)
      } catch (error) {
        this.error = error.message
        console.error('删除知识项失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 获取 Markdown 内容
    async fetchMarkdownContent(id) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.getMarkdownContent(id)
        this.markdownContent = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('获取 Markdown 内容失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新 Markdown 内容
    async updateMarkdownContent(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.updateMarkdownContent(id, data)
        this.markdownContent = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('更新 Markdown 内容失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新 Markdown 知识项
    async updateMarkdown(id, data) {
      return this.updateKnowledgeItem(id, data)
    },

    // 获取网页内容
    async fetchWebpageContent(id) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.getWebpageContent(id)
        this.webpageContent = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('获取网页内容失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新网页内容
    async updateWebpageContent(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.updateWebpageContent(id, data)
        this.webpageContent = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('更新网页内容失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新网页知识项
    async updateWebpage(id, data) {
      return this.updateKnowledgeItem(id, data)
    },

    // 抓取网页
    async fetchWebpage(data) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.fetchWebpage(data)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('抓取网页失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 抓取并更新网页内容
    async fetchAndUpdateWebpage(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.fetchAndUpdateWebpage(id, data)
        this.webpageContent = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('抓取并更新网页内容失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 添加标签到知识项
    async addTagToKnowledge(knowledgeId, tagId) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.addTagToKnowledge(knowledgeId, tagId)
        // 更新本地知识项
        const index = this.knowledgeItems.findIndex(item => item.id === knowledgeId)
        if (index !== -1) {
          this.knowledgeItems[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('添加标签失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 从知识项移除标签
    async removeTagFromKnowledge(knowledgeId, tagId) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.removeTagFromKnowledge(knowledgeId, tagId)
        // 更新本地知识项
        const index = this.knowledgeItems.findIndex(item => item.id === knowledgeId)
        if (index !== -1) {
          this.knowledgeItems[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('移除标签失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 抓取网页内容（用于新建网页知识项）
    async fetchWebpageContent(url) {
      this.loading = true
      this.error = null
      try {
        const response = await knowledgeService.fetchWebpage({ url })
        this.fetchedWebpageContent = response.data.content
        return response.data.content
      } catch (error) {
        this.error = error.message
        console.error('抓取网页内容失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
