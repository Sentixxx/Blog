import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {path: '/login',component:() => import("@/views/login/Index.vue")},
  {path: '/register',component: () => import("@/views/register/Index.vue")},
  {path: '/home',component:() => import('@/views/Index.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})
export default router
