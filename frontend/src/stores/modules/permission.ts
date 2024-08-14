import { RouteRecordRaw } from 'vue-router'
import { store } from '@/stores'

export const usePermissionStore = defineStore('permission', () => {
    //应用中所有的路由列表，包括静态路由和动态路由
    const routes = ref<RouteRecordRaw[]>([])

    return {
        routes
    }
})

export function usePermissionStoreHook() {
    return usePermissionStore(store)
}
