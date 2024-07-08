import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import Elementplus from 'element-plus'
import axios from '@/api/axios'


const app = createApp(App)

app.use(router)
app.config.globalProperties.$axios = axios;
app.use(Elementplus)
app.mount('#app')

import 'element-plus/theme-chalk/index.css'
