<template>
    <div :class="{ 'has-logo': sidebarLogo }">
        <template v-if="layout == LayoutEnum.LEFT || LayoutEnum.TOP">
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
