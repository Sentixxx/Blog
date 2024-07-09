import { RouteRecordRaw } from "vue-router";
import { constantRoutes } from "@/router";
import { store } from "@/stores";
import MenuAPI , { RouteView } from "@/api/menu";

const moduels = import.meta.glob("@/views/**/**.vue");

const Layout = () => import("@/layout/Index.vue");

export const usePermissionStore = defineStore("permission", () => {
    //应用中所有的路由列表，包括静态路由和动态路由
    const routes = ref<RouteRecordRaw[]>([]);
    // 混合模式左侧菜单列表
    const mixLeftMenus = ref<RouteView[]>([]);
})
