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
        :router="true"
    >
        <el-menu-item
            index="/home"
            @select="handleHome"
            :class="{ 'submenu-title-noDropdown': true }"
        >
            <el-icon><House /></el-icon>
            <template #title><span>首页</span> </template>
        </el-menu-item>
        <el-menu-item index="/books" @select="handleBook">
            <el-icon><Notebook /></el-icon>
            <template #title><span>图书</span> </template>
        </el-menu-item>
        <el-menu-item index="/self" @select="handleUser">
            <el-icon><User /></el-icon>
            <template #title><span>个人信息</span> </template>
        </el-menu-item>
    </el-menu>
</template>

<script setup lang="ts">
import { useAppStore, useSettingsStore } from '@/stores'

import { LayoutEnum } from '@/enums/layoutEnum'
import { computed } from 'vue'
import variables from '@/styles/variables.module.scss'
import { House, Notebook, User } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()

const settingsStore = useSettingsStore()
const appStore = useAppStore()
const currentRoute = useRoute()

const mode = computed(() => (settingsStore.layout === LayoutEnum.TOP ? 'horizontal' : 'vertical'))

function handleHome() {
    router.push('/home')
}

function handleBook() {
    router.push('/book')
}

function handleUser() {
    router.push('/user')
    console.log('user')
}

function handleSystem() {
    router.push('/system')
}
</script>

<style lang="scss"></style>
