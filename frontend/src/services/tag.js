import request from '../utils/request'

// 标签 API 服务
const tagService = {
  // 获取标签列表
  getTags: (params) => {
    return request({
      url: '/tags',
      method: 'get',
      params
    })
  },

  // 获取单个标签
  getTag: (id) => {
    return request({
      url: `/tags/${id}`,
      method: 'get'
    })
  },

  // 创建标签
  createTag: (data) => {
    return request({
      url: '/tags',
      method: 'post',
      data
    })
  },

  // 更新标签
  updateTag: (id, data) => {
    return request({
      url: `/tags/${id}`,
      method: 'put',
      data
    })
  },

  // 删除标签
  deleteTag: (id) => {
    return request({
      url: `/tags/${id}`,
      method: 'delete'
    })
  }
}

export default tagService
