import request from '../utils/request'

// 文件夹 API 服务
const folderService = {
  // 获取文件夹列表
  getFolders: (params) => {
    return request({
      url: '/folders',
      method: 'get',
      params
    })
  },

  // 获取文件夹树结构
  getFolderTree: (rootId) => {
    return request({
      url: '/folders/tree',
      method: 'get',
      params: { rootId }
    })
  },

  // 获取单个文件夹
  getFolder: (id) => {
    return request({
      url: `/folders/${id}`,
      method: 'get'
    })
  },

  // 创建文件夹
  createFolder: (data) => {
    return request({
      url: '/folders',
      method: 'post',
      data
    })
  },

  // 更新文件夹
  updateFolder: (id, data) => {
    return request({
      url: `/folders/${id}`,
      method: 'put',
      data
    })
  },

  // 删除文件夹
  deleteFolder: (id) => {
    return request({
      url: `/folders/${id}`,
      method: 'delete'
    })
  }
}

export default folderService
