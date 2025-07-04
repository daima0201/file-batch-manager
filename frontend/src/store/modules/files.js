import api from '@/services/api'

const state = {
  files: [],
  currentPath: null,
  operations: [],
  breadcrumbPaths: []
}

const mutations = {
  SET_FILES(state, files) {
    state.files = files
  },
  SET_CURRENT_PATH(state, path) {
    state.currentPath = path
  },
  SET_OPERATIONS(state, operations) {
    state.operations = operations
  },
  SET_BREADCRUMB_PATHS(state, paths) {
    state.breadcrumbPaths = paths
  }
}

const actions = {
  async loadFiles({ commit, state }, parentPath = null) {
    try {
      const params = parentPath ? { parent_path: parentPath } : {}
      const response = await api.get('/files/', { params })
      commit('SET_FILES', response.data)
      commit('SET_CURRENT_PATH', parentPath)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async fetchOperationHistory({ commit }) {
    try {
      const response = await api.get('/operations/')
      commit('SET_OPERATIONS', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async startScan({ commit }, { path, scanHidden }) {
    try {
      await api.post('/scan/', {
        root_path: path,
        scan_hidden: scanHidden
      })
      return true
    } catch (error) {
      throw error
    }
  },

  async deleteFiles({ commit, dispatch, state }, fileIds) {
    try {
      const response = await api.post('/file-ops/delete_files/', {
        file_ids: fileIds
      })
      dispatch('loadFiles', state.currentPath)
      dispatch('fetchOperationHistory')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async moveFiles({ commit, dispatch, state }, { fileIds, targetDir }) {
    try {
      const response = await api.post('/file-ops/move_files/', {
        file_ids: fileIds,
        target_dir: targetDir
      })
      dispatch('loadFiles', state.currentPath)
      dispatch('fetchOperationHistory')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async renameFile({ commit, dispatch, state }, { fileId, newName }) {
    try {
      const response = await api.post('/file-ops/rename_file/', {
        file_id: fileId,
        new_name: newName
      })
      dispatch('loadFiles', state.currentPath)
      dispatch('fetchOperationHistory')
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}