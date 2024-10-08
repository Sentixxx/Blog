<template>
    <el-drawer v-model="settingsVisible" size="300" :title="$t('navbar.settings.project')">
        <el-divider>{{ $t('navbar.settings.theme') }}</el-divider>

        <div class="flex-center">
            <el-switch v-model="isDark" active-icon="Moon" inactive-icon="Sunny" @change="changeTheme" />
        </div>

        <el-divider>{{ $t('settings.interface') }}</el-divider>

        <div class="setting-item">
            <span class="text-xs">{{ $t('settings.themeColor') }}</span>
            <ThemeColorPicker v-model="settingsStore.themeColor" @update:model-value="changeThemeColor" />
        </div>

        <div class="setting-item">
            <span class="text-xs">{{ $t('settings.tagsView') }}</span>
            <el-switch v-model="settingsStore.tagsView" />
        </div>

        <div class="setting-item">
            <span class="text-xs">{{ $t('settings.fixedHeader') }}</span>
            <el-switch v-model="settingsStore.fixedHeader" />
        </div>

        <div class="setting-item">
            <span class="text-xs">{{ $t('settings.sidebarLogo') }}</span>
            <el-switch v-model="settingsStore.sidebarLogo" />
        </div>

        <el-divider>{{ $t('settings.navigation') }}</el-divider>

        <LayoutSelect v-model="settingsStore.layout" @update:model-value="changeLayout" />
    </el-drawer>
</template>

<script setup lang="ts">
import { useSettingsStore, useAppStore } from '@/stores'
import { LayoutEnum } from '@/enums/layoutEnum'
import { ThemeEnum } from '@/enums/themeEnum'

const route = useRoute()
const appStore = useAppStore()
const settingsStore = useSettingsStore()

const settingsVisible = computed({
    get() {
        return settingsStore.settingsVisible
    },
    set() {
        settingsStore.settingsVisible = false
    }
})

/** 切换主题颜色 */
function changeThemeColor(color: string) {
    settingsStore.setThemeColor(color)
}

/** 切换主题 */
const isDark = ref<boolean>(settingsStore.themeMode === ThemeEnum.DARK)
const changeTheme = (val: any) => {
    isDark.value = val
    settingsStore.setThemeMode(isDark.value ? ThemeEnum.DARK : ThemeEnum.LIGHT)
}

/** 切换布局 */
function changeLayout(layout: string) {
    settingsStore.setLayout(layout)
}

/** 递归查找最外层父节点 */
function findOutermostParent(tree: any[], findName: string) {
    let parentMap: any = {}

    function buildParentMap(node: any, parent: any) {
        parentMap[node.name] = parent

        if (node.children) {
            for (let i = 0; i < node.children.length; i++) {
                buildParentMap(node.children[i], node)
            }
        }
    }

    for (let i = 0; i < tree.length; i++) {
        buildParentMap(tree[i], null)
    }

    let currentNode = parentMap[findName]
    while (currentNode) {
        if (!parentMap[currentNode.name]) {
            return currentNode
        }
        currentNode = parentMap[currentNode.name]
    }

    return null
}
</script>

<style lang="scss" scoped>
.setting-item {
    @apply py-1 flex-x-between;
}
</style>
