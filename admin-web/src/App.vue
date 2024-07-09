<template>
    <el-config-provider :locale="locale" :size="size">
        <el-watermark
            v-if="watermarkEnabled"
            :font="{ color: fontColor }"
            :content="defaultSettings.watermarkContent"
            :z-index="9999"
            class="wh-full"
        >
            <router-view />
        </el-watermark>
        <router-view v-else />
    </el-config-provider>
</template>

<script setup lang="ts">
import { useAppStore, useSettingsStore } from '@/stores'
import defaultSettings from './config/settings'
import { ThemeEnum } from './enums/themeEnum'
import { SizeEnum } from './enums/sizeEnum'

const appStore = useAppStore()
const settingsStore = useSettingsStore()

const locale = computed(() => appStore.locale)
const size = computed(() => appStore.size as SizeEnum)
const watermarkEnabled = computed(() => settingsStore.watermarkEnabled)

const fontColor = computed(() => {
    return settingsStore.themeMode === ThemeEnum.DARK ? 'rgba(255,255,255,.15)' : 'rgba(0,0,0,.15)'
})
</script>
