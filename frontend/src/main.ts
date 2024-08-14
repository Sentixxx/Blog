import { createApp } from 'vue'
import App from './App.vue'

import 'virtual:svg-icons-register'

import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/styles/index.scss'

import 'animate.css'
import 'uno.css'

import setupPlugins from '@/config/index'
const app = createApp(App)

app.use(setupPlugins)
app.mount('#app')
