import api from './api'

export default {
  login(credentials) {
    return api.post('/token/', credentials)
  },
  refreshToken(refresh) {
    return api.post('/token/refresh/', { refresh })
  },
  logout() {
    return api.post('/token/blacklist/', {})
  }
}