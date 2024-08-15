<template>
    <section class="app-main" :style="{ minHeight }">
        <router-view>
            <template #default="{ Component, route }">
                <transition enter-active-class="animate__animated animate_fadeIn" mode="out-in">
                    <keep-alive :include="cachedViews">
                        <component :is="Component" :key="route.path" />
                    </keep-alive>
                </transition>
            </template>
        </router-view>
    </section>
</template>
<script setup lang="ts">
import { useSettingsStore, useTagsViewStore } from '@/stores'
import variables from '@/styles/variables.module.scss'

const cachedViews = computed(() => useTagsViewStore().cachedViews)
const minHeight = computed(() => {
    if (useSettingsStore().tagsView) {
        return `calc(100vh - ${variables['navbar-height']} - ${variables['tags-view-height']})`
    } else {
        return `calc(100vh - ${variables['navbar-height']})`
    }
})
</script>
<style lang="scss" scoped>
.app-main {
    position: relative;
    background-color: var(--el-bg-color-page);
}
</style>
