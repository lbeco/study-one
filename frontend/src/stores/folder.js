import { defineStore } from 'pinia'
import folderService from '../services/folder'

// 文件夹状态管理
export const useFolderStore = defineStore('folder', {
  state: () => ({
    folders: [],
    folderTree: [],
    currentFolder: null,
    loading: false,
    error: null
  }),

  getters: {
    getFolderById: (state) => (id) => {
      return state.folders.find(folder => folder.id === id)
    }
  },

  actions: {
    // 获取文件夹列表
    async fetchFolders(params) {
      this.loading = true
      this.error = null
      try {
        const response = await folderService.getFolders(params)
        this.folders = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取文件夹列表失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 获取文件夹树
    async fetchFolderTree(rootId) {
      this.loading = true
      this.error = null
      try {
        const response = await folderService.getFolderTree(rootId)
        this.folderTree = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取文件夹树失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 获取单个文件夹
    async fetchFolder(id) {
      this.loading = true
      this.error = null
      try {
        const response = await folderService.getFolder(id)
        this.currentFolder = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取文件夹失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 创建文件夹
    async createFolder(data) {
      this.loading = true
      this.error = null
      try {
        const response = await folderService.createFolder(data)
        this.folders.push(response.data)
        // 重新获取文件夹树
        await this.fetchFolderTree(null)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('创建文件夹失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新文件夹
    async updateFolder(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await folderService.updateFolder(id, data)
        const index = this.folders.findIndex(folder => folder.id === id)
        if (index !== -1) {
          this.folders[index] = response.data
        }
        // 重新获取文件夹树
        await this.fetchFolderTree(null)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('更新文件夹失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 删除文件夹
    async deleteFolder(id) {
      this.loading = true
      this.error = null
      try {
        await folderService.deleteFolder(id)
        this.folders = this.folders.filter(folder => folder.id !== id)
        // 重新获取文件夹树
        await this.fetchFolderTree(null)
      } catch (error) {
        this.error = error.message
        console.error('删除文件夹失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
