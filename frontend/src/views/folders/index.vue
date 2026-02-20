<template>
  <div class="folders-management">
    <div class="page-header">
      <h2 class="page-title">文件夹管理</h2>
      <el-button type="primary" icon="Plus" @click="handleCreateFolder">
        新建文件夹
      </el-button>
    </div>

    <!-- 文件夹树 -->
    <div class="folder-tree-container">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>文件夹结构</span>
            <el-icon><Folder /></el-icon>
          </div>
        </template>
        <div class="tree-content">
          <el-tree
            v-if="folderTree.length > 0"
            :data="folderTree"
            :props="treeProps"
            :expand-on-click-node="false"
            @node-click="handleNodeClick"
            @node-contextmenu="handleContextMenu"
            class="folder-tree"
          >
            <template #default="{ node, data }">
              <div class="tree-node">
                <span @click="handleNodeClick(data)">{{ node.label }}</span>
                <div class="node-actions" v-show="node.expanded">
                  <el-button size="small" text @click.stop="handleCreateSubFolder(data.id)">
                    <el-icon><Plus /></el-icon>
                  </el-button>
                  <el-button size="small" text @click.stop="handleEditFolder(data)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" text type="danger" @click.stop="handleDeleteFolder(data.id)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
          </el-tree>
          <div v-else class="empty-state">
            <el-empty description="暂无文件夹" />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 新建/编辑文件夹对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="400px"
    >
      <el-form :model="folderForm" label-width="80px">
        <el-form-item label="文件夹名称">
          <el-input v-model="folderForm.name" placeholder="请输入文件夹名称" />
        </el-form-item>
        <el-form-item label="父文件夹">
          <el-select v-model="folderForm.parent_id" placeholder="选择父文件夹">
            <el-option label="根文件夹" value="" />
            <el-option
              v-for="folder in folders"
              :key="folder.id"
              :label="folder.name"
              :value="folder.id"
              :disabled="folder.id === currentFolderId"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveFolder">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFolderStore } from '../../stores/folder'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const folderStore = useFolderStore()

const folderTree = ref([])
const folders = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新建文件夹')
const currentFolderId = ref(null)

const treeProps = {
  children: 'children',
  label: 'name'
}

const folderForm = reactive({
  name: '',
  parent_id: ''
})

// 初始化数据
onMounted(async () => {
  await fetchFolderData()
})

// 获取文件夹数据
const fetchFolderData = async () => {
  await folderStore.fetchFolderTree(null)
  folderTree.value = folderStore.folderTree
  
  await folderStore.fetchFolders({ page: 1, page_size: 100 })
  folders.value = folderStore.folders
}

// 节点点击
const handleNodeClick = (data) => {
  router.push({
    path: '/knowledge',
    query: { folder_id: data.id }
  })
}

// 右键菜单
const handleContextMenu = (event, node, data) => {
  event.preventDefault()
  // 可以在这里实现右键菜单逻辑
}

// 新建文件夹
const handleCreateFolder = () => {
  dialogTitle.value = '新建文件夹'
  folderForm.name = ''
  folderForm.parent_id = ''
  currentFolderId.value = null
  dialogVisible.value = true
}

// 新建子文件夹
const handleCreateSubFolder = (parentId) => {
  dialogTitle.value = '新建子文件夹'
  folderForm.name = ''
  folderForm.parent_id = parentId
  currentFolderId.value = null
  dialogVisible.value = true
}

// 编辑文件夹
const handleEditFolder = (data) => {
  dialogTitle.value = '编辑文件夹'
  folderForm.name = data.name
  folderForm.parent_id = data.parent_id || ''
  currentFolderId.value = data.id
  dialogVisible.value = true
}

// 删除文件夹
const handleDeleteFolder = async (folderId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文件夹吗？删除后，文件夹内的知识项将移至根目录。', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await folderStore.deleteFolder(folderId)
    await fetchFolderData()
    ElMessage.success('删除文件夹成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除文件夹失败')
    }
  }
}

// 保存文件夹
const saveFolder = async () => {
  if (!folderForm.name) {
    ElMessage.error('请输入文件夹名称')
    return
  }

  try {
    const data = {
      name: folderForm.name,
      parent_id: folderForm.parent_id || null
    }

    if (currentFolderId.value) {
      // 编辑文件夹
      await folderStore.updateFolder(currentFolderId.value, data)
      ElMessage.success('更新文件夹成功')
    } else {
      // 新建文件夹
      await folderStore.createFolder(data)
      ElMessage.success('创建文件夹成功')
    }

    dialogVisible.value = false
    await fetchFolderData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>

<style scoped>
.folders-management {
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

.folder-tree-container {
  margin-top: 20px;
}

.tree-content {
  min-height: 400px;
}

.folder-tree {
  border: none;
}

.tree-node {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.node-actions {
  display: flex;
  gap: 4px;
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
}
</style>