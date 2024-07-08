import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {path: '/login',component:() => import("@/views/system/login/Index.vue"),name:'登录'},
  {path: '/register',component: () => import("@/views/system/register/Index.vue"),name:'注册'},
  {path: '/home',component:() => import('@/views/system/Index.vue'),name: '主页'},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})
export default router
