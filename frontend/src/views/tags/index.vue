<template>
  <div class="tags-management">
    <div class="page-header">
      <h2 class="page-title">标签管理</h2>
      <el-button type="primary" icon="Plus" @click="handleCreateTag">
        新建标签
      </el-button>
    </div>

    <!-- 标签列表 -->
    <div class="tags-container">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>标签列表</span>
            <el-icon><CollectionTag /></el-icon>
          </div>
        </template>
        <div class="tags-content">
          <div v-if="tags.length > 0" class="tags-grid">
            <el-card
              v-for="tag in tags"
              :key="tag.id"
              class="tag-card"
              :body-style="{ padding: '16px' }"
            >
              <div class="tag-info">
                <el-tag :size="'large'" :color="tag.color" class="tag-display">
                  {{ tag.name }}
                </el-tag>
                <div class="tag-meta">
                  <span class="tag-count">{{ tag.count || 0 }} 个知识项</span>
                </div>
              </div>
              <div class="tag-actions">
                <el-button size="small" @click="handleEditTag(tag)">
                  编辑
                </el-button>
                <el-button size="small" type="danger" @click="handleDeleteTag(tag.id)">
                  删除
                </el-button>
              </div>
            </el-card>
          </div>
          <div v-else class="empty-state">
            <el-empty description="暂无标签" />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 新建/编辑标签对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="400px"
    >
      <el-form :model="tagForm" label-width="80px">
        <el-form-item label="标签名称">
          <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="标签颜色">
          <el-color-picker v-model="tagForm.color" show-alpha />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveTag">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useTagStore } from '../../stores/tag'
import { ElMessage, ElMessageBox } from 'element-plus'

const tagStore = useTagStore()

const tags = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新建标签')
const currentTagId = ref(null)

const tagForm = reactive({
  name: '',
  color: '#409eff'
})

// 初始化数据
onMounted(async () => {
  await fetchTagData()
})

// 获取标签数据
const fetchTagData = async () => {
  await tagStore.fetchTags({ page: 1, page_size: 100 })
  tags.value = tagStore.tags
}

// 新建标签
const handleCreateTag = () => {
  dialogTitle.value = '新建标签'
  tagForm.name = ''
  tagForm.color = '#409eff'
  currentTagId.value = null
  dialogVisible.value = true
}

// 编辑标签
const handleEditTag = (tag) => {
  dialogTitle.value = '编辑标签'
  tagForm.name = tag.name
  tagForm.color = tag.color
  currentTagId.value = tag.id
  dialogVisible.value = true
}

// 删除标签
const handleDeleteTag = async (tagId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个标签吗？删除后，该标签将从所有知识项中移除。', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await tagStore.deleteTag(tagId)
    await fetchTagData()
    ElMessage.success('删除标签成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除标签失败')
    }
  }
}

// 保存标签
const saveTag = async () => {
  if (!tagForm.name) {
    ElMessage.error('请输入标签名称')
    return
  }

  try {
    const data = {
      name: tagForm.name,
      color: tagForm.color
    }

    if (currentTagId.value) {
      // 编辑标签
      await tagStore.updateTag(currentTagId.value, data)
      ElMessage.success('更新标签成功')
    } else {
      // 新建标签
      await tagStore.createTag(data)
      ElMessage.success('创建标签成功')
    }

    dialogVisible.value = false
    await fetchTagData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>

<style scoped>
.tags-management {
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

.tags-container {
  margin-top: 20px;
}

.tags-content {
  min-height: 400px;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.tag-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag-info {
  flex: 1;
}

.tag-display {
  font-size: 16px;
  padding: 8px 16px;
}

.tag-meta {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.tag-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .tags-grid {
    grid-template-columns: 1fr;
  }
  
  .tag-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .tag-actions {
    align-self: flex-end;
  }
}
</style>