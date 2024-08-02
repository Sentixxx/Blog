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
        <el-menu-item index="/home">
            <el-icon class="icon"><House /></el-icon>
            <template #title><span>首页</span> </template>
        </el-menu-item>
        <el-menu-item index="/books">
            <el-icon><Notebook /></el-icon>
            <template #title><span>图书</span> </template>
        </el-menu-item>
        <el-menu-item index="/borrow" v-if="userStore.user.user_instance_id != -1">
            <el-icon><User /></el-icon>
            <template #title><span>借阅记录</span> </template>
        </el-menu-item>
        <el-sub-menu index="" v-if="isAdmin()">
            <template #title>
                <el-icon><Setting /></el-icon>
                <span>管理</span>
            </template>
            <el-menu-item index="/manage/user" v-if="isAdmin()">
                <template #title>
                    <el-icon><User /></el-icon>
                    <span>用户管理</span>
                </template>
            </el-menu-item>
            <el-menu-item index="/manage/book" v-if="isAdmin()">
                <template #title>
                    <el-icon><Notebook /></el-icon>
                    <span>图书管理</span>
                </template>
            </el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script setup lang="ts">
import { useAppStore, useSettingsStore } from '@/stores'

import { LayoutEnum } from '@/enums/layoutEnum'
import { computed } from 'vue'
import variables from '@/styles/variables.module.scss'
import { House, Notebook, User, Setting } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { isAdmin } from '@/utils/perm'
const router = useRouter()

const settingsStore = useSettingsStore()
const userStore = useUserStore()
const appStore = useAppStore()
const currentRoute = useRoute()

const mode = computed(() => (settingsStore.layout === LayoutEnum.TOP ? 'horizontal' : 'vertical'))
</script>

<style lang="scss">
.hideSidebar {
}
</style>
