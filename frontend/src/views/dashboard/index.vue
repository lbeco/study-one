<template>
  <div class="dashboard">
    <h2 class="page-title">仪表盘</h2>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>知识项总数</span>
            <el-icon><Document /></el-icon>
          </div>
        </template>
        <div class="stat-value">{{ knowledgeCount }}</div>
      </el-card>

      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>文件夹数</span>
            <el-icon><Folder /></el-icon>
          </div>
        </template>
        <div class="stat-value">{{ folderCount }}</div>
      </el-card>

      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>标签数</span>
            <el-icon><CollectionTag /></el-icon>
          </div>
        </template>
        <div class="stat-value">{{ tagCount }}</div>
      </el-card>
    </div>

    <!-- 最近知识项 -->
    <el-card class="recent-knowledge">
      <template #header>
        <div class="card-header">
          <span>最近创建/修改的知识项</span>
          <el-button type="primary" text @click="viewAllKnowledge">查看全部</el-button>
        </div>
      </template>
      <div v-if="recentKnowledge.length > 0">
        <el-table :data="recentKnowledge" style="width: 100%">
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="type" label="类型" />
          <el-table-column prop="updated_at" label="更新时间">
            <template #default="scope">
              {{ formatDate(scope.row.updated_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button size="small" @click="viewKnowledge(scope.row.id)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-state">
        <el-empty description="暂无知识项" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useKnowledgeStore } from '../../stores/knowledge'
import { useFolderStore } from '../../stores/folder'
import { useTagStore } from '../../stores/tag'

const router = useRouter()
const knowledgeStore = useKnowledgeStore()
const folderStore = useFolderStore()
const tagStore = useTagStore()

const knowledgeCount = ref(0)
const folderCount = ref(0)
const tagCount = ref(0)
const recentKnowledge = ref([])

// 初始化数据
onMounted(async () => {
  // 获取知识项列表
  await knowledgeStore.fetchKnowledgeItems({ page: 1, page_size: 5 })
  recentKnowledge.value = knowledgeStore.knowledgeItems
  knowledgeCount.value = knowledgeStore.knowledgeItems.length

  // 获取文件夹列表
  await folderStore.fetchFolders({ page: 1, page_size: 100 })
  folderCount.value = folderStore.folders.length

  // 获取标签列表
  await tagStore.fetchTags({ page: 1, page_size: 100 })
  tagCount.value = tagStore.tags.length
})

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 查看知识项
const viewKnowledge = (id) => {
  router.push(`/knowledge/markdown/${id}`)
}

// 查看全部知识项
const viewAllKnowledge = () => {
  router.push('/knowledge')
}
</script>

<style scoped>
.dashboard {
  min-height: 100%;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
  margin-top: 10px;
}

.recent-knowledge {
  margin-top: 20px;
}

.empty-state {
  padding: 40px 0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
