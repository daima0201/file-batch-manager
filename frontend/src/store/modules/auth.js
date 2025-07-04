import authService from '@/services/auth'
import router from '@/router'

const state = {
  user: null,
  token: localStorage.getItem('token') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  isAuthenticated: !!localStorage.getItem('token')
}

const mutations = {
  SET_USER(state, user) {
    state.user = user
  },
  SET_TOKEN(state, { access, refresh }) {
    state.token = access
    state.refreshToken = refresh
    state.isAuthenticated = true
    localStorage.setItem('token', access)
    localStorage.setItem('refreshToken', refresh)
  },
  LOGOUT(state) {
    state.user = null
    state.token = null
    state.refreshToken = null
    state.isAuthenticated = false
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await authService.login(credentials)
      commit('SET_TOKEN', response.data)

      // 获取用户信息
      // 这里假设后端有获取当前用户信息的API
      // const userResponse = await api.get('/users/me/')
      // commit('SET_USER', userResponse.data)

      router.push('/')
      return true
    } catch (error) {
      throw error
    }
  },

  async refreshToken({ commit, state }) {
    if (!state.refreshToken) return

    try {
      const response = await authService.refreshToken(state.refreshToken)
      commit('SET_TOKEN', response.data)
      return true
    } catch (error) {
      commit('LOGOUT')
      router.push('/login')
      return false
    }
  },

  async logout({ commit }) {
    try {
      await authService.logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
    commit('LOGOUT')
    router.push('/login')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}