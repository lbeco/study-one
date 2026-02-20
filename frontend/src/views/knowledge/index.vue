<template>
  <div class="knowledge-list">
    <div class="page-header">
      <h2 class="page-title">知识项管理</h2>
      <el-button type="primary" icon="Plus" @click="handleCreateKnowledge">
        新建知识项
      </el-button>
    </div>

    <!-- 筛选工具栏 -->
    <div class="toolbar">
      <el-select v-model="filter.folder_id" placeholder="选择文件夹" class="filter-item">
        <el-option label="所有文件夹" value="" />
        <el-option
          v-for="folder in folders"
          :key="folder.id"
          :label="folder.name"
          :value="folder.id"
        />
      </el-select>

      <el-select v-model="filter.type" placeholder="选择类型" class="filter-item">
        <el-option label="所有类型" value="" />
        <el-option label="Markdown" value="markdown" />
        <el-option label="网页" value="webpage" />
      </el-select>

      <el-button type="primary" plain @click="handleSearch">
        筛选
      </el-button>
    </div>

    <!-- 知识项列表 -->
    <div class="knowledge-grid">
      <el-card
        v-for="item in knowledgeItems"
        :key="item.id"
        class="knowledge-card"
        @click="handleKnowledgeClick(item)
      >
        <template #header>
          <div class="card-header">
            <span class="card-title">{{ item.title }}</span>
            <el-tag size="small" :type="item.type === 'markdown' ? 'primary' : 'success'">
              {{ item.type === 'markdown' ? 'Markdown' : '网页' }}
            </el-tag>
          </div>
        </template>
        
        <div class="card-body">
          <div class="tags-container">
            <el-tag
              v-for="tag in item.tags"
              :key="tag.id"
              :color="tag.color"
              size="small"
              class="tag-item"
            >
              {{ tag.name }}
            </el-tag>
          </div>
          <div class="card-footer">
            <span class="update-time">{{ formatDate(item.updated_at) }}</span>
            <div class="card-actions">
              <el-button size="small" text @click.stop="handleEditKnowledge(item)">
                编辑
              </el-button>
              <el-button size="small" text type="danger" @click.stop="handleDeleteKnowledge(item.id)">
                删除
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 空状态 -->
    <div v-if="knowledgeItems.length === 0" class="empty-state">
      <el-empty description="暂无知识项" />
    </div>

    <!-- 分页 -->
    <div v-if="knowledgeItems.length > 0" class="pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 创建知识项对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新建知识项"
      width="500px"
    >
      <el-form :model="knowledgeForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="knowledgeForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="knowledgeForm.type" placeholder="请选择类型">
            <el-option label="Markdown" value="markdown" />
            <el-option label="网页" value="webpage" />
          </el-select>
        </el-form-item>
        <el-form-item label="文件夹">
          <el-select v-model="knowledgeForm.folder_id" placeholder="请选择文件夹">
            <el-option label="根文件夹" value="" />
            <el-option
              v-for="folder in folders"
              :key="folder.id"
              :label="folder.name"
              :value="folder.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createKnowledge">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useKnowledgeStore } from '../../stores/knowledge'
import { useFolderStore } from '../../stores/folder'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const knowledgeStore = useKnowledgeStore()
const folderStore = useFolderStore()

const knowledgeItems = ref([])
const folders = ref([])
const total = ref(0)
const dialogVisible = ref(false)

const filter = reactive({
  folder_id: '',
  type: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20
})

const knowledgeForm = reactive({
  title: '',
  type: 'markdown',
  folder_id: ''
})

// 初始化数据
onMounted(async () => {
  // 获取文件夹列表
  await folderStore.fetchFolders({ page: 1, page_size: 100 })
  folders.value = folderStore.folders

  // 检查路由参数
  const folderId = route.query.folder_id
  const tagIds = route.query.tag_ids
  const searchQuery = route.query.q

  if (folderId) {
    filter.folder_id = folderId
  }

  // 获取知识项列表
  await fetchKnowledgeItems()
})

// 获取知识项列表
const fetchKnowledgeItems = async () => {
  const params = {
    page: pagination.page,
    page_size: pagination.pageSize,
    folder_id: filter.folder_id || undefined,
    type: filter.type || undefined
  }

  await knowledgeStore.fetchKnowledgeItems(params)
  knowledgeItems.value = knowledgeStore.knowledgeItems
  total.value = knowledgeStore.knowledgeItems.length
}

// 筛选
const handleSearch = async () => {
  pagination.page = 1
  await fetchKnowledgeItems()
}

// 分页处理
const handleSizeChange = async (size) => {
  pagination.pageSize = size
  await fetchKnowledgeItems()
}

const handleCurrentChange = async (current) => {
  pagination.page = current
  await fetchKnowledgeItems()
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 创建知识项
const handleCreateKnowledge = () => {
  dialogVisible.value = true
}

const createKnowledge = async () => {
  if (!knowledgeForm.title) {
    ElMessage.error('请输入标题')
    return
  }

  try {
    const data = {
      title: knowledgeForm.title,
      type: knowledgeForm.type,
      folder_id: knowledgeForm.folder_id || null
    }

    await knowledgeStore.createKnowledgeItem(data)
    dialogVisible.value = false
    await fetchKnowledgeItems()
    ElMessage.success('创建知识项成功')

    // 重置表单
    knowledgeForm.title = ''
    knowledgeForm.type = 'markdown'
    knowledgeForm.folder_id = ''
  } catch (error) {
    ElMessage.error('创建知识项失败')
  }
}

// 点击知识项
const handleKnowledgeClick = (item) => {
  if (item.type === 'markdown') {
    router.push(`/knowledge/markdown/${item.id}`)
  } else {
    router.push(`/knowledge/webpage/${item.id}`)
  }
}

// 编辑知识项
const handleEditKnowledge = (item) => {
  if (item.type === 'markdown') {
    router.push(`/knowledge/markdown/${item.id}`)
  } else {
    router.push(`/knowledge/webpage/${item.id}`)
  }
}

// 删除知识项
const handleDeleteKnowledge = async (id) => {
  try {
    await knowledgeStore.deleteKnowledgeItem(id)
    await fetchKnowledgeItems()
    ElMessage.success('删除知识项成功')
  } catch (error) {
    ElMessage.error('删除知识项失败')
  }
}

// 监听路由参数变化
watch(
  () => route.query,
  async (newQuery) => {
    if (newQuery.folder_id) {
      filter.folder_id = newQuery.folder_id
      await fetchKnowledgeItems()
    }
  },
  { deep: true }
)
</script>

<style scoped>
.knowledge-list {
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  color: #303133;
}

.toolbar {
  background-color: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-item {
  width: 150px;
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.knowledge-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.knowledge-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tags-container {
  margin: 10px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}

.update-time {
  font-size: 12px;
  color: #909399;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

@media (max-width: 768px) {
  .knowledge-grid {
    grid-template-columns: 1fr;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-item {
    width: 100%;
  }
}
</style>
