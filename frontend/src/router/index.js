import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/dashboard/index.vue'),
      meta: { title: '仪表盘' }
    },
    {
      path: '/folders',
      name: 'folders',
      component: () => import('../views/folders/index.vue'),
      meta: { title: '文件夹管理' }
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('../views/knowledge/index.vue'),
      meta: { title: '知识项管理' }
    },
    {
      path: '/knowledge/markdown/:id',
      name: 'markdown-edit',
      component: () => import('../views/markdown/index.vue'),
      meta: { title: 'Markdown 编辑' }
    },
    {
      path: '/knowledge/webpage/:id',
      name: 'webpage-edit',
      component: () => import('../views/webpage/index.vue'),
      meta: { title: '网页内容编辑' }
    },
    {
      path: '/tags',
      name: 'tags',
      component: () => import('../views/tags/index.vue'),
      meta: { title: '标签管理' }
    }
  ]
})

// 全局前置守卫，设置页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'study-one'} - study-one`
  next()
})

export default router
