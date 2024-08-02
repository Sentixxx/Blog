import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'
import request from '@/utils/request'
import { AxiosResponse } from 'axios'

export const Layout = () => import('@/layout/index.vue')

export const constantRoutes: Array<RouteRecordRaw> = [
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
        redirect: '/home',
        children: [
            {
                path: 'home',
                component: () => import('@/views/home/index.vue'),
                name: 'Home',
                meta: {
                    title: 'Home',
                    icon: 'homepage',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '/books',
                component: () => import('@/views/book/index.vue'),
                meta: {
                    title: 'Books',
                    icon: 'book',
                    affix: true,
                    KeepAlive: true
                },
                children: [
                    {
                        path: 'info/:id',
                        component: () => import('@/views/book/components/bookInfoDialog.vue'),
                        meta: {
                            title: 'default_book_id',
                            affix: true,
                            keepAlive: true
                        },
                        beforeEnter: async (to, from, next) => {
                            try {
                                console.log(to.params.id)
                                const res: [any] = await request({
                                    url: '/book/info',
                                    params: { book_id: to.params.id },
                                    method: 'get'
                                })
                                if (res.length > 0) {
                                    to.meta.title = res[0].book_name
                                    next()
                                } else {
                                    next({ path: '/404' })
                                }
                            } catch (error) {
                                console.error(error)
                                next({ path: '/404' })
                            }
                        }
                    }
                ]
            },
            {
                path: '/self',
                component: () => import('@/views/user/index.vue'),
                meta: {
                    title: 'User',
                    icon: 'user',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '/borrow',
                component: () => import('@/views/borrow/index.vue'),
                meta: {
                    title: 'Borrow',
                    icon: 'borrow',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '/manage/user',
                component: () => import('@/views/manage/userManage.vue'),
                meta: {
                    title: 'UserManage',
                    icon: 'manage',
                    affix: true,
                    KeepAlive: true
                }
            },
            {
                path: '/manage/book',
                component: () => import('@/views/manage/bookManage.vue'),
                meta: {
                    title: 'BookManage',
                    icon: 'manage',
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
