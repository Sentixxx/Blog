<template>
    <div :class="{ 'has-logo': sidebarLogo }">
        <div class="flex w-full" v-if="layout == LayoutEnum.MIX">
            <SidebarLogo v-if="sidebarLogo" :collapse="!appStore.sidebar.opened" />
            <SidebarMixTopMenu class="flex-1" />
        </div>
        <template v-else>
            <el-scrollbar>
                <SidebarMenu :menuList="permissionStore.routes" basePath="" />
            </el-scrollbar>
        </template>
    </div>
</template>

<script setup lang="ts">
import { useSettingsStore, useAppStore, usePermissionStore } from '@/stores'
import { LayoutEnum } from '@/enums/layoutEnum'

const permissionStore = usePermissionStore()
const settingsStore = useSettingsStore()
const appStore = useAppStore()
const sidebarLogo = computed(() => settingsStore.sidebarLogo)
const layout = computed(() => settingsStore.layout)
</script>

<style lang="scss" scoped>
.has-logo {
    .el-scrollbar {
        height: calc(100vh - $navbar-height);
    }
}
</style>
