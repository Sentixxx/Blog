import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'


export const Layout = () => import('@/layout/Index.vue');

export const contantRoutes: RouteRecordRaw[] = [
    {
        path: '/redirect',
        component: Layout,
        children: [
            {
                path: "/redirect/:path(.*)",
                component: () => import('@/views/redirect/Index.vue'),
            },
        ],
    },
    {
        path: '/login',
        component: () => import('@/views/system/login/Index.vue'),
        meta: { hidden: true },
    },
    {
        path: "/",
        name: "/",
        component: Layout,
        redirect: "/dashboard",
        children: [
            {
                path: "dashboard",
                component: () => import('@/views/dashboard/Index.vue'),
                name: "Dashboard",
                meta: {
                    title: "Dashboard",
                    icon: "homepage",
                    affix: true,
                    KeepAlive: true,
                },
            },
        ]
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes: contantRoutes,
    scrollBehavior: () => ({ left: 0, top: 0 }),
});

export function setupRouter(app: App<Element>) {
    app.use(router);
}

export function resetRouter() {
    router.replace({path: "/login"});
}

export default router
