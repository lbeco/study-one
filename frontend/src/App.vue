<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <el-header height="60px" class="app-header">
      <div class="header-left">
        <el-avatar size="small" icon="Document" />
        <h1 class="app-title">{{ appTitle }}</h1>
      </div>
      <div class="header-center">
        <el-input
          v-model="searchQuery"
          placeholder="搜索知识项..."
          prefix-icon="Search"
          clearable
          @keyup.enter="handleSearch"
          class="search-input"
        />
      </div>
      <div class="header-right">
        <el-dropdown>
          <el-button circle>
            <el-icon><Setting /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>设置</el-dropdown-item>
              <el-dropdown-item>关于</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <div class="app-body">
      <!-- 侧边栏 -->
      <el-aside width="250px" class="app-sidebar">
        <!-- 快捷操作 -->
        <div class="sidebar-section">
          <h3 class="section-title">快捷操作</h3>
          <el-button type="primary" plain icon="Plus" @click="handleCreateKnowledge">
            新建知识项
          </el-button>
        </div>

        <!-- 文件夹树 -->
        <div class="sidebar-section">
          <h3 class="section-title">文件夹</h3>
          <el-tree
            v-if="folderTree.length > 0"
            :data="folderTree"
            :props="treeProps"
            @node-click="handleFolderClick"
            class="folder-tree"
          />
          <div v-else class="empty-state">
            <el-empty description="暂无文件夹" />
          </div>
        </div>

        <!-- 标签列表 -->
        <div class="sidebar-section">
          <h3 class="section-title">标签</h3>
          <el-tag
            v-for="tag in tags"
            :key="tag.id"
            :color="tag.color"
            @click="handleTagClick(tag.id)"
            class="tag-item"
          >
            {{ tag.name }}
          </el-tag>
          <div v-if="tags.length === 0" class="empty-state">
            <el-empty description="暂无标签" />
          </div>
        </div>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFolderStore } from './stores/folder'
import { useTagStore } from './stores/tag'

const router = useRouter()
const folderStore = useFolderStore()
const tagStore = useTagStore()

const appTitle = ref('study-one')
const searchQuery = ref('')
const folderTree = ref([])
const tags = ref([])

const treeProps = {
  children: 'children',
  label: 'name'
}

// 初始化数据
onMounted(async () => {
  await folderStore.fetchFolderTree(null)
  folderTree.value = folderStore.folderTree
  
  await tagStore.fetchTags()
  tags.value = tagStore.tags
})

// 搜索处理
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/knowledge',
      query: { q: searchQuery.value }
    })
  }
}

// 创建知识项
const handleCreateKnowledge = () => {
  // 这里可以打开一个对话框让用户选择知识项类型
  router.push('/knowledge')
}

// 文件夹点击
const handleFolderClick = (data) => {
  router.push({
    path: '/knowledge',
    query: { folder_id: data.id }
  })
}

// 标签点击
const handleTagClick = (tagId) => {
  router.push({
    path: '/knowledge',
    query: { tag_ids: tagId }
  })
}
</script>

<style scoped>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

/* 顶部导航栏 */
.app-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.app-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
  color: #303133;
}

.search-input {
  width: 300px;
}

/* 主体内容 */
.app-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 侧边栏 */
.app-sidebar {
  background-color: #fff;
  border-right: 1px solid #ebeef5;
  padding: 20px;
  overflow-y: auto;
}

.sidebar-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 14px;
  font-weight: bold;
  color: #909399;
  margin: 0 0 12px 0;
}

.folder-tree {
  border: none;
}

.tag-item {
  margin: 4px;
  cursor: pointer;
}

.empty-state {
  padding: 20px 0;
}

/* 主内容区 */
.app-main {
  padding: 20px;
  overflow-y: auto;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-sidebar {
    display: none;
  }
  
  .search-input {
    width: 200px;
  }
}
</style>
