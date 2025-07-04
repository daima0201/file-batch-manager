import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import files from './modules/files'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    files
  }
})