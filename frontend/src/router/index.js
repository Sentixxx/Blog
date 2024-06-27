import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '../views/register/RegisterView.vue'
import LoginView from '../views/login/LoginView.vue'

const routes = [
  {path: '/',component:LoginView},
  {path: '/register',component:RegisterView},
  {path: '/home',component:() => import('../views/HomeView.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})
export default router
