<template>
    <div class="wh-full" :class="classObj">
        <!--遮罩-->
        <div
            v-if="isMobile && isOpenSidebar"
            class="wh-full fixed-lt z-999 bg-black bg-opacity-30"
            @click="handleOutsideClick"
        ></div>

        <!--侧边栏-->
        <Sidebar class="sidebar-container" />

        <!--混合布局-->
        <div v-if="layout === LayoutEnum.MIX" class="mix-container">
            <div class="mix-container-left"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useAppStore, useSettingsStore } from '@/stores'
import defaultSettings from '@/config/settings'
import { DeviceEnum } from '@/enums/deviceEnum'
import { LayoutEnum } from '@/enums/layoutEnum'

const appStore = useAppStore()
const settingsStore = useSettingsStore()
const width = useWindowSize().width
const WIDTH_DESKTOP = 992 // 响应式布局容器固定宽度  大屏（>=1200px） 中屏（>=992px） 小屏（>=768px）
const isMobile = computed(() => appStore.device === DeviceEnum.MOBILE)
const isOpenSidebar = computed(() => appStore.sidebar.opened)
const fixedHeader = computed(() => settingsStore.fixedHeader)
const showTagsView = computed(() => settingsStore.tagsView)
const layout = computed(() => settingsStore.layout)
const activeTopMenuPath = computed(() => appStore.activeTopMenuPath)

watch(
    () => activeTopMenuPath.value
    (newVal) => {
        permissionStore.setMixLeftMenus(newVal);
    },
    {deep:true,immedite:true});
</script>
