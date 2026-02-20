import request from '../utils/request'

// 知识项 API 服务
const knowledgeService = {
  // 获取知识项列表
  getKnowledgeItems: (params) => {
    return request({
      url: '/knowledge',
      method: 'get',
      params
    })
  },

  // 搜索知识项
  searchKnowledge: (params) => {
    return request({
      url: '/knowledge/search',
      method: 'get',
      params
    })
  },

  // 按标签查询知识项
  getKnowledgeByTags: (params) => {
    return request({
      url: '/knowledge/by-tags',
      method: 'get',
      params
    })
  },

  // 获取单个知识项
  getKnowledgeItem: (id) => {
    return request({
      url: `/knowledge/${id}`,
      method: 'get'
    })
  },

  // 创建知识项
  createKnowledgeItem: (data) => {
    return request({
      url: '/knowledge',
      method: 'post',
      data
    })
  },

  // 更新知识项
  updateKnowledgeItem: (id, data) => {
    return request({
      url: `/knowledge/${id}`,
      method: 'put',
      data
    })
  },

  // 删除知识项
  deleteKnowledgeItem: (id) => {
    return request({
      url: `/knowledge/${id}`,
      method: 'delete'
    })
  },

  // 添加标签到知识项
  addTagToKnowledge: (knowledgeId, tagId) => {
    return request({
      url: `/knowledge/${knowledgeId}/tags/${tagId}`,
      method: 'post'
    })
  },

  // 从知识项移除标签
  removeTagFromKnowledge: (knowledgeId, tagId) => {
    return request({
      url: `/knowledge/${knowledgeId}/tags/${tagId}`,
      method: 'delete'
    })
  },

  // 获取 Markdown 内容
  getMarkdownContent: (id) => {
    return request({
      url: `/knowledge/${id}/markdown`,
      method: 'get'
    })
  },

  // 更新 Markdown 内容
  updateMarkdownContent: (id, data) => {
    return request({
      url: `/knowledge/${id}/markdown`,
      method: 'put',
      data
    })
  },

  // 上传 Markdown 文件
  uploadMarkdownFile: (id, file) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('item_id', id)
    
    return request({
      url: '/knowledge/markdown/upload',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取网页内容
  getWebpageContent: (id) => {
    return request({
      url: `/knowledge/${id}/webpage`,
      method: 'get'
    })
  },

  // 创建/更新网页内容
  updateWebpageContent: (id, data) => {
    return request({
      url: `/knowledge/${id}/webpage`,
      method: 'post',
      data
    })
  },

  // 抓取网页
  fetchWebpage: (data) => {
    return request({
      url: '/knowledge/webpage/fetch',
      method: 'post',
      data
    })
  },

  // 抓取并更新网页内容
  fetchAndUpdateWebpage: (id, data) => {
    return request({
      url: `/knowledge/${id}/webpage/fetch`,
      method: 'post',
      data
    })
  }
}

export default knowledgeService
