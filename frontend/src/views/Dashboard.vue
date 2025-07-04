<script>
export default {
  name: "FileItem.vue"
}
</script>

<template>
  <div class="dashboard">
    <div class="header">
      <h1><font-awesome-icon icon="folder-tree" /> 文件管理系统</h1>
      <div class="user-info">
        <span>{{ user.username }}</span>
        <button @click="logout" class="btn"><font-awesome-icon icon="sign-out-alt" /> 退出</button>
      </div>
    </div>

    <div class="main-content">
      <div class="sidebar">
        <Breadcrumb :paths="breadcrumbPaths" @navigate="navigateToDirectory" />
        <div class="file-tree">
          <FileItem
            v-for="file in files"
            :key="file.id"
            :file="file"
            @select="selectFile"
            @dblclick="openDirectory(file)"
          />
        </div>
        <button class="btn primary scan-btn" @click="showScanModal = true">
          <font-awesome-icon icon="sync" /> 扫描文件系统
        </button>
      </div>

      <div class="content">
        <OperationPanel
          :selectedFiles="selectedFiles"
          @delete="deleteFiles"
          @move="moveFiles"
          @rename="renameFile"
        />

        <div class="operations-history">
          <h2>操作历史</h2>
          <HistoryList :operations="operations" />
        </div>
      </div>
    </div>

    <ScanModal
      v-if="showScanModal"
      @confirm="startScan"
      @cancel="showScanModal = false"
    />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb.vue'
import FileItem from '@/components/FileItem.vue'
import OperationPanel from '@/components/OperationPanel.vue'
import HistoryList from '@/components/HistoryList.vue'
import ScanModal from '@/components/ScanModal.vue'

export default {
  components: {
    Breadcrumb,
    FileItem,
    OperationPanel,
    HistoryList,
    ScanModal
  },
  data() {
    return {
      selectedFiles: [],
      showScanModal: false
    }
  },
  computed: {
    ...mapState({
      files: state => state.files.files,
      operations: state => state.files.operations,
      breadcrumbPaths: state => state.files.breadcrumbPaths,
      user: state => state.auth.user
    })
  },
  mounted() {
    this.loadRootDirectory()
    this.fetchOperationHistory()
  },
  methods: {
    ...mapActions('files', [
      'loadFiles',
      'fetchOperationHistory',
      'startScan',
      'deleteFiles',
      'moveFiles',
      'renameFile'
    ]),
    ...mapActions('auth', ['logout']),

    loadRootDirectory() {
      this.$store.commit('files/SET_BREADCRUMB_PATHS', [])
      this.loadFiles(null)
    },

    navigateToDirectory(path) {
      if (!path) {
        this.loadRootDirectory()
        return
      }

      const pathParts = path.split('/').filter(p => p)
      const breadcrumbPaths = []

      let current = ''
      for (let i = 0; i < pathParts.length; i++) {
        current += (i > 0 ? '/' : '') + pathParts[i]
        breadcrumbPaths.push({
          name: pathParts[i],
          path: current
        })
      }

      this.$store.commit('files/SET_BREADCRUMB_PATHS', breadcrumbPaths)
      this.loadFiles(path)
    },

    selectFile(file) {
      this.selectedFiles = [file.id]
    },

    openDirectory(file) {
      if (file.type === 'directory') {
        this.navigateToDirectory(file.path)
      }
    },

    startScan({ path, scanHidden }) {
      this.showScanModal = false
      this.startScan({ path, scanHidden })
        .then(() => {
          this.$toast.success('扫描完成')
          this.loadRootDirectory()
        })
        .catch(error => {
          this.$toast.error(`扫描失败: ${error.message}`)
        })
    },

    deleteFiles() {
      if (!this.selectedFiles.length || !confirm('确定删除选中的文件/目录吗？')) return;

      this.deleteFiles(this.selectedFiles)
        .then(() => {
          this.$toast.success('删除成功')
          this.selectedFiles = []
        })
        .catch(error => {
          this.$toast.error(`删除失败: ${error.message}`)
        })
    },

    moveFiles(targetDir) {
      if (!targetDir || !this.selectedFiles.length) {
        this.$toast.warning('请输入目标路径')
        return
      }

      this.moveFiles({ fileIds: this.selectedFiles, targetDir })
        .then(() => {
          this.$toast.success('移动成功')
          this.selectedFiles = []
        })
        .catch(error => {
          this.$toast.error(`移动失败: ${error.message}`)
        })
    },

    renameFile(newName) {
      if (this.selectedFiles.length !== 1) return
      if (!newName) {
        this.$toast.warning('请输入新名称')
        return
      }

      this.renameFile({ fileId: this.selectedFiles[0], newName })
        .then(() => {
          this.$toast.success('重命名成功')
          this.selectedFiles = []
        })
        .catch(error => {
          this.$toast.error(`重命名失败: ${error.message}`)
        })
    }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn.primary {
  background: #3498db;
  color: white;
}

.btn.danger {
  background: #e74c3c;
  color: white;
}

.main-content {
  display: flex;
  flex: 1;
  padding: 20px;
  gap: 20px;
  overflow: hidden;
}

.sidebar {
  width: 30%;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.file-tree {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.scan-btn {
  margin: 15px;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.operations-history {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.operations-history h2 {
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}
</style>