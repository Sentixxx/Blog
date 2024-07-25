<template>
    <div class="flex">
        <template v-if="!isMobile">
            <!--全屏 -->
            <div class="nav-action-item" @click="toggle">
                <el-tooltip :content="$t('navbar.fullscreen')" effect="dark" placement="bottom">
                    <svg-icon :icon-class="isFullscreen ? 'fullscreen-exit' : 'fullscreen'" />
                </el-tooltip>
            </div>
            <!-- 布局大小 -->
            <el-tooltip :content="$t('navbar.sizeSelect')" effect="dark" placement="bottom">
                <size-select class="nav-action-item" />
            </el-tooltip>

            <!-- 语言选择 -->
            <el-tooltip :content="$t('navbar.langSelect')" effect="dark" placement="bottom">
                <lang-select class="nav-action-item" />
            </el-tooltip>

            <!-- 消息通知 -->
            <el-tooltip :content="$t('navbar.notice')" effect="dark" placement="bottom">
                <el-dropdown class="message nav-action-item" trigger="click">
                    <el-badge is-dot>
                        <div class="flex-center h100% p10px">
                            <i-ep-bell />
                        </div>
                    </el-badge>
                    <template #dropdown>
                        <div class="px-5 py-2">
                            <el-tabs v-model="activeTab">
                                <el-tab-pane
                                    v-for="(label, key) in MessageTypeLabels"
                                    :label="label"
                                    :name="key"
                                    :key="key"
                                >
                                    <div
                                        class="w-[380px] py-2"
                                        v-for="message in getFilteredMessages(key)"
                                        :key="message.id"
                                    >
                                        <el-link type="primary">
                                            <el-text class="w-350px" size="default" truncated>
                                                {{ message.title }}</el-text
                                            >
                                        </el-link>
                                    </div>
                                </el-tab-pane>
                            </el-tabs>
                            <el-divider />
                            <div class="flex-x-between">
                                <el-link type="primary" :underline="false">
                                    <span class="text-xs">查看更多</span
                                    ><el-icon class="text-xs"><ArrowRight /></el-icon
                                ></el-link>
                                <el-link type="primary" :underline="false">
                                    <span class="text-xs">全部已读</span></el-link
                                >
                            </div>
                        </div>
                    </template>
                </el-dropdown>
            </el-tooltip>
        </template>

        <!-- 用户头像 -->
        <el-dropdown class="nav-action-item" trigger="click">
            <div class="flex-center h100% p10px">
                <img
                    :src="userStore.user.avatar + '?imageView2/1/w/80/h/80'"
                    class="rounded-full mr-10px w24px w24px"
                />
                <span>{{ userStore.user.username }}</span>
            </div>
            <template #dropdown>
                <el-dropdown-menu>
                    <a target="_blank" href="https://gitee.com/youlaiorg/vue3-element-admin">
                        <el-dropdown-item>{{ $t('navbar.gitee') }}</el-dropdown-item>
                    </a>
                    <a target="_blank" href="https://juejin.cn/post/7228990409909108793">
                        <el-dropdown-item>{{ $t('navbar.document') }}</el-dropdown-item>
                    </a>
                    <el-dropdown-item divided @click="logout">
                        {{ $t('navbar.logout') }}
                    </el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>

        <!-- 设置 -->
        <template v-if="defaultSettings.showSettings">
            <div class="nav-action-item" @click="settingStore.settingsVisible = true">
                <svg-icon icon-class="setting" />
            </div>
        </template>
    </div>
</template>
<script setup lang="ts">
import { useAppStore, useTagsViewStore, useUserStore, useSettingsStore } from '@/stores'
import defaultSettings from '@/config/settings'
import { DeviceEnum } from '@/enums/deviceEnum'
import { MessageTypeEnum, MessageTypeLabels } from '@/enums/messageTypeEnum'
import { ElMessageBox } from 'element-plus'

const appStore = useAppStore()
const tagsViewStore = useTagsViewStore()
const userStore = useUserStore()
const settingStore = useSettingsStore()

const route = useRoute()
const router = useRouter()

const isMobile = computed(() => appStore.device === DeviceEnum.MOBILE)

const { isFullscreen, toggle } = useFullscreen()

const activeTab = ref(MessageTypeEnum.MESSAGE)

const messages = ref([
    {
        id: 1,
        title: '重要提醒：请定期更改您的密码以保证账户安全。',
        type: MessageTypeEnum.MESSAGE
    }
])

const getFilteredMessages = (type: MessageTypeEnum) => {
    return messages.value.filter((message: any) => message.type === type)
}

/* 注销 */
function logout() {
    ElMessageBox.confirm('确定注销并退出系统吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        lockScroll: false
    }).then(() => {
        userStore
            .logout()
            .then(() => {
                tagsViewStore.delAllViews()
            })
            .then(() => {
                router.push(`/login?redirect=${route.fullPath}`)
            })
    })
}
</script>
<style lang="scss" scoped>
.nav-action-item {
    display: inline-block;
    min-width: 40px;
    height: $navbar-height;
    line-height: $navbar-height;
    color: var(--el-text-color);
    text-align: center;
    cursor: pointer;

    &:hover {
        background: rgb(0 0 0 / 10%);
    }
}

:deep(.message .el-badge__content.is-fixed.is-dot) {
    top: 5px;
    right: 10px;
}

:deep(.el-divider--horizontal) {
    margin: 10px 0;
}

.dark .nav-action-item:hover {
    background: rgb(255 255 255 / 20%);
}

.see-more {
    padding: 10px 0;
    text-align: center;
}

.see-more a {
    color: var(--el-color-primary);
    text-decoration: none;
}
</style>
