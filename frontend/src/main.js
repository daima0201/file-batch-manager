import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faFolder, faFile, faSync, faSearch,
  faTrash, faEdit, faArrowRight,
  faSignOutAlt, faSignInAlt
} from '@fortawesome/free-solid-svg-icons'
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';

library.add(faFolder, faFile, faSync, faSearch, faTrash, faEdit, faArrowRight, faSignOutAlt, faSignInAlt)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(VueAxios, axios)
Vue.use(VueToast)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')