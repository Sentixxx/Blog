import { RouteRecordRaw } from 'vue-router'
import { constantRoutes } from '@/router'
import { store } from '@/stores'
import MenuAPI, { RouteView } from '@/api/menu'

const moduels = import.meta.glob('@/views/**/**.vue')

const Layout = () => import('@/layout/index.vue')

export const usePermissionStore = defineStore('permission', () => {
    //应用中所有的路由列表，包括静态路由和动态路由
    const routes = ref<RouteRecordRaw[]>([])

    function generateRoutes() {
        return new Promise<RouteRecordRaw[]>((resolve, reject) => {
            MenuAPI.getRoutes()
                .then((data) => {
                    const dynamicRoutes = transformRoutes(data)
                    routes.value = constantRoutes.concat(dynamicRoutes)
                    resolve(dynamicRoutes)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    }

    return {
        routes,
        generateRoutes
    }
})

const transformRoutes = (routes: RouteView[]) => {
    const asysncRoutes: RouteRecordRaw[] = []
    routes.forEach((route) => {
        const tmpRoute = { ...route } as RouteRecordRaw
        if (tmpRoute.component?.toString() == 'Layout') {
            tmpRoute.component = Layout
        } else {
            const component = moduels['@/views/${tmpRoute.component}.vue']
            if (component) {
                tmpRoute.component = component
            } else {
                // tmpRoute.component = () => import("@/views/error-page/404.vue");
            }
        }
        if (tmpRoute.children) {
            tmpRoute.children = transformRoutes(route.children)
        }

        asysncRoutes.push(tmpRoute)
    })
    return asysncRoutes
}

export function usePermissionStoreHook() {
    return usePermissionStore(store)
}
