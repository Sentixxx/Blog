<template>
    <el-menu
        :default-active="currentRoute.path"
        :collapse="!appStore.sidebar.opened"
        :background-color="variables['menu-background']"
        :text-color="variables['menu-text']"
        :active-text-color="variables['menu-active-text']"
        :unique-opened="false"
        :collapse-transition="false"
        :mode="mode"
    >
        <SidebarMenuItem
            v-for="route in menuList"
            :key="route.path"
            :item="route"
            :basePath="resolvePath(route.path, basePath)"
        />
    </el-menu>
</template>

<script setup lang="ts">
import { useAppStore, useSettingsStore } from '@/stores'

import { LayoutEnum } from '@/enums/layoutEnum'
import { computed } from 'vue'
import { resolvePath } from '@/utils/path'
import variables from '@/styles/variables.module.scss'

const settingsStore = useSettingsStore()
const appStore = useAppStore()
const currentRoute = useRoute()

const props = defineProps({
    menuList: {
        required: true,
        default: () => {
            return []
        },
        type: Array<any>
    },
    basePath: {
        required: true,
        default: '',
        type: String
    }
})
const mode = computed(() => (settingsStore.layout === LayoutEnum.TOP ? 'horizontal' : 'vertical'))
</script>
