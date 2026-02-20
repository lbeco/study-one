<template>
  <div class="webpage-edit">
    <div class="page-header">
      <el-button type="primary" plain @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <el-input v-model="title" placeholder="请输入标题" class="title-input" />
      <div class="header-actions">
        <el-button @click="handleRefresh">
          刷新内容
        </el-button>
        <el-button type="primary" @click="handleSave">
          保存
        </el-button>
      </div>
    </div>

    <!-- 编辑区域 -->
    <div class="editor-container">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="编辑">
          <div class="editor-wrapper">
            <div class="url-section">
              <el-input v-model="url" placeholder="请输入网页URL" class="url-input" />
              <el-button type="primary" @click="fetchWebpageContent">
                获取内容
              </el-button>
            </div>
            <div class="content-section">
              <el-input
                v-model="content"
                type="textarea"
                :rows="20"
                placeholder="请输入网页内容"
                class="content-input"
              />
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="预览">
          <div class="preview-wrapper">
            <div class="webpage-preview" v-html="previewContent" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 右侧工具栏 -->
    <div class="sidebar">
      <!-- 标签管理 -->
      <div class="sidebar-section">
        <h3 class="section-title">标签</h3>
        <div class="tags-container">
          <el-tag
            v-for="tag in selectedTags"
            :key="tag.id"
            :color="tag.color"
            class="tag-item"
          >
            {{ tag.name }}
            <el-button size="small" @click="removeTag(tag.id)">
              <el-icon><Close /></el-icon>
            </el-button>
          </el-tag>
          <el-button type="primary" plain size="small" @click="showTagSelector = true">
            添加标签
          </el-button>
        </div>
      </div>

      <!-- 文件夹选择 -->
      <div class="sidebar-section">
        <h3 class="section-title">文件夹</h3>
        <el-select v-model="folderId" placeholder="选择文件夹" class="folder-select">
          <el-option label="根文件夹" value="" />
          <el-option
            v-for="folder in folders"
            :key="folder.id"
            :label="folder.name"
            :value="folder.id"
          />
        </el-select>
      </div>

      <!-- 元数据 -->
      <div class="sidebar-section">
        <h3 class="section-title">元数据</h3>
        <div class="meta-item">
          <span class="meta-label">创建时间:</span>
          <span class="meta-value">{{ formatDate(createdAt) }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">更新时间:</span>
          <span class="meta-value">{{ formatDate(updatedAt) }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">最后抓取:</span>
          <span class="meta-value">{{ formatDate(lastFetched) }}</span>
        </div>
      </div>
    </div>

    <!-- 标签选择器 -->
    <el-dialog
      v-model="showTagSelector"
      title="选择标签"
      width="400px"
    >
      <el-checkbox-group v-model="selectedTagIds">
        <el-checkbox
          v-for="tag in allTags"
          :key="tag.id"
          :label="tag.id"
          class="tag-checkbox"
        >
          <el-tag :color="tag.color" class="tag-checkbox-label">
            {{ tag.name }}
          </el-tag>
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showTagSelector = false">取消</el-button>
          <el-button type="primary" @click="confirmTags">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useKnowledgeStore } from '../../stores/knowledge'
import { useTagStore } from '../../stores/tag'
import { useFolderStore } from '../../stores/folder'
import { ElMessage, ElLoading } from 'element-plus'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const knowledgeStore = useKnowledgeStore()
const tagStore = useTagStore()
const folderStore = useFolderStore()

const id = route.params.id
const title = ref('')
const url = ref('')
const content = ref('')
const folderId = ref('')
const createdAt = ref('')
const updatedAt = ref('')
const lastFetched = ref('')
const activeTab = ref('edit')
const showTagSelector = ref(false)

const folders = ref([])
const allTags = ref([])
const selectedTags = ref([])
const selectedTagIds = ref([])

const previewContent = computed(() => {
  return marked(content.value || '')
})

// 初始化
onMounted(async () => {
  await fetchInitialData()
})

// 获取初始数据
const fetchInitialData = async () => {
  // 获取文件夹列表
  await folderStore.fetchFolders({ page: 1, page_size: 100 })
  folders.value = folderStore.folders

  // 获取标签列表
  await tagStore.fetchTags({ page: 1, page_size: 100 })
  allTags.value = tagStore.tags

  // 如果是编辑模式，获取现有数据
  if (id) {
    await knowledgeStore.fetchKnowledgeItem(id)
    const item = knowledgeStore.currentKnowledgeItem
    if (item) {
      title.value = item.title
      url.value = item.url
      content.value = item.content
      folderId.value = item.folder_id || ''
      createdAt.value = item.created_at
      updatedAt.value = item.updated_at
      lastFetched.value = item.last_fetched
      selectedTags.value = item.tags || []
      selectedTagIds.value = selectedTags.value.map(tag => tag.id)
    }
  }
}

// 返回
const goBack = () => {
  router.push('/knowledge')
}

// 保存
const handleSave = async () => {
  if (!title.value.trim()) {
    ElMessage.error('请输入标题')
    return
  }

  if (!url.value.trim()) {
    ElMessage.error('请输入网页URL')
    return
  }

  try {
    const data = {
      title: title.value,
      url: url.value,
      content: content.value,
      folder_id: folderId.value || null,
      tag_ids: selectedTagIds.value
    }

    if (id) {
      // 更新
      await knowledgeStore.updateWebpage(id, data)
      ElMessage.success('更新成功')
    } else {
      // 新建
      await knowledgeStore.createKnowledgeItem({
        ...data,
        type: 'webpage'
      })
      ElMessage.success('创建成功')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 刷新内容
const handleRefresh = async () => {
  if (!url.value.trim()) {
    ElMessage.error('请输入网页URL')
    return
  }
  await fetchWebpageContent()
}

// 获取网页内容
const fetchWebpageContent = async () => {
  if (!url.value.trim()) {
    ElMessage.error('请输入网页URL')
    return
  }

  const loading = ElLoading.service({
    lock: true,
    text: '正在获取网页内容...',
    background: 'rgba(0, 0, 0, 0.7)'
  })

  try {
    // 调用后端API获取网页内容
    await knowledgeStore.fetchWebpageContent(url.value)
    const fetchedContent = knowledgeStore.fetchedWebpageContent
    if (fetchedContent) {
      content.value = fetchedContent
      ElMessage.success('获取网页内容成功')
    }
  } catch (error) {
    ElMessage.error('获取网页内容失败')
  } finally {
    loading.close()
  }
}

// 移除标签
const removeTag = (tagId) => {
  const index = selectedTagIds.value.indexOf(tagId)
  if (index > -1) {
    selectedTagIds.value.splice(index, 1)
  }
  selectedTags.value = allTags.value.filter(tag => selectedTagIds.value.includes(tag.id))
}

// 确认标签选择
const confirmTags = () => {
  selectedTags.value = allTags.value.filter(tag => selectedTagIds.value.includes(tag.id))
  showTagSelector.value = false
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}
</script>

<style scoped>
.webpage-edit {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 20px;
  gap: 16px;
}

.title-input {
  flex: 1;
  font-size: 18px;
  font-weight: bold;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.editor-container {
  flex: 1;
  display: flex;
  margin-right: 280px;
}

.editor-wrapper {
  flex: 1;
  height: calc(100vh - 180px);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.url-section {
  display: flex;
  gap: 12px;
}

.url-input {
  flex: 1;
}

.content-section {
  flex: 1;
  overflow: hidden;
}

.content-input {
  width: 100%;
  height: 100%;
  resize: none;
}

.preview-wrapper {
  flex: 1;
  height: calc(100vh - 180px);
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}

.webpage-preview {
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.8;
}

.sidebar {
  position: fixed;
  right: 0;
  top: 80px;
  width: 260px;
  height: calc(100vh - 80px);
  background-color: #fff;
  border-left: 1px solid #ebeef5;
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

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag-item {
  margin-bottom: 8px;
}

.folder-select {
  width: 100%;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}

.meta-label {
  color: #909399;
}

.meta-value {
  color: #303133;
}

.tag-checkbox {
  display: block;
  margin-bottom: 8px;
  width: 100%;
}

.tag-checkbox-label {
  margin-right: 8px;
}

@media (max-width: 1024px) {
  .sidebar {
    display: none;
  }
  
  .editor-container {
    margin-right: 0;
  }
  
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .url-section {
    flex-direction: column;
  }
}
</style>