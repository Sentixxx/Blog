import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'

export const Layout = () => import('@/layout/index.vue')

export const constantRoutes: RouteRecordRaw[] = [
    {
        path: '/redirect',
        component: Layout,
        children: [
            {
                path: '/redirect/:path(.*)',
                component: () => import('@/views/redirect/index.vue')
            }
        ]
    },
    {
        path: '/login',
        component: () => import('@/views/login/index.vue'),
        meta: { hidden: true }
    },
    {
        path: '/register',
        component: () => import('@/views/register/index.vue'),
        meta: { hidden: true }
    },
    {
        path: '/',
        name: '/',
        component: Layout,
        redirect: '/dashboard',
        children: [
            {
                path: 'dashboard',
                component: () => import('@/views/dashboard/index.vue'),
                name: 'Dashboard',
                meta: {
                    title: 'Dashboard',
                    icon: 'homepage',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '/book',
                component: () => import('@/views/book/index.vue'),
                meta: {
                    title: 'Book',
                    icon: 'book',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '/user',
                component: () => import('@/views/user/index.vue'),
                meta: {
                    title: 'User',
                    icon: 'user',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '401',
                component: () => import('@/views/error-page/401.vue'),
                meta: { hidden: true }
            },
            {
                path: '404',
                component: () => import('@/views/error-page/404.vue'),
                meta: { hidden: true }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: constantRoutes,
    scrollBehavior: () => ({ left: 0, top: 0 })
})

export function setupRouter(app: App<Element>) {
    app.use(router)
}

export function resetRouter() {
    router.replace({ path: '/login' })
}

export default router
