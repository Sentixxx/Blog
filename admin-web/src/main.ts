import { createApp } from 'vue'
import App from './App.vue'

import 'virtual:svg-icons-register'

import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/styles/index.scss'

import 'animate.css'
import 'uno.css'

import setupPlugins from '@/config/index'
import cors from 'cors'
const app = createApp(App)

// const corsOptions = {
//     origin: 'http://127.0.0.1/', // 允许的域名
//     optionsSuccessStatus: 200
// }

app.use(setupPlugins)
// app.use(cors(corsOptions))
app.mount('#app')
