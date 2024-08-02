<template>
    <div class="home-container">
        <el-card shadow="never">
            <el-row justify="space-between">
                <el-col :span="18" :xs="24">
                    <div class="flex h-full items-center">
                        <img
                            class="w-20 h-20 mr-5 rounded-full"
                            :src="userStore.user.user_instance_avatar + '?imageView2/1/w/80/h/80'"
                        />
                        <div>
                            <p>{{ greetings }}</p>
                            <p class="text-sm text-gray"></p>
                        </div>
                    </div>
                </el-col>

                <!-- <el-col :span="6" :xs="24">
                    <div class="flex h-full items-center justify-around">
                        <el-statistic
                            v-for="item in statisticData"
                            :key="item.key"
                            :value="item.value"
                        >
                            <template #title>
                                <div class="flex items-center">
                                    <svg-icon :icon-class="item.iconClass" size="20px" />
                                    <span class="text-[16px] ml-1">{{ item.title }}</span>
                                </div>
                            </template>
                            <template v-if="item.suffix" #suffix>/100</template>
                        </el-statistic>
                    </div>
                </el-col> -->
            </el-row>
        </el-card>

        <!-- 数据卡片 -->
        <el-row :gutter="10" class="mt-5">
            <el-col :xs="24" :sm="12" :lg="6">
                <el-card shadow="never">
                    <template #header>
                        <div class="flex-x-between">
                            <span class="text-[var(--el-text-color-secondary)]">馆内当前藏书</span>
                            <el-tag type="success" size="small">-</el-tag>
                        </div>
                    </template>

                    <div class="flex-x-between mt-2">
                        <span class="text-lg"> {{ booknum }}</span>
                        <svg-icon icon-class="ip" size="2em" />
                    </div>
                    <div class="flex-x-between mt-2 text-sm text-[var(--el-text-color-secondary)]">
                        <span> 总图书数 </span>
                        <span> {{ totalbooknum }}</span>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts">
defineOptions({
    name: 'Dashboard',
    inheritAttrs: false
})

import BookAPI from '@/api/book'
import BookInstanceAPI from '@/api/bookInstance'
import { useUserStore } from '@/stores'
import { c } from 'vite/dist/node/types.d-aGj9QkWt'

const userStore = useUserStore()

const date: Date = new Date()

function getUserNickname() {
    if (userStore.user.user_instance_nickname == null) return userStore.user.user_instance_name
    return userStore.user.user_instance_nickname
}
const greetings = computed(() => {
    const hours = date.getHours()
    if (hours >= 6 && hours < 8) {
        return '晨起披衣出草堂，轩窗已自喜微凉🌅！'
    } else if (hours >= 8 && hours < 12) {
        return '上午好，' + getUserNickname() + '！'
    } else if (hours >= 12 && hours < 18) {
        return '下午好，' + getUserNickname() + '！'
    } else if (hours >= 18 && hours < 24) {
        return '晚上好，' + getUserNickname() + '！'
    } else {
        return '偷偷向银河要了一把碎星，只等你闭上眼睛撒入你的梦中，晚安🌛！'
    }
})

const booknum = ref(0)

const totalbooknum = ref(0)

async function getBookNum() {
    const res = await BookInstanceAPI.getAll()

    totalbooknum.value = res.length
    const bookRes = await BookAPI.getAll()

    for (let i = 0; i < bookRes.length; i++) {
        booknum.value += bookRes[i]?.book_cur_stock_num ?? 0
    }
}

// 右上角数量
const statisticData = ref([
    {
        value: 99,
        iconClass: 'message',
        title: '消息',
        key: 'message'
    },
    {
        value: 50,
        iconClass: 'todo',
        title: '待办',
        suffix: '/100',
        key: 'upcoming'
    },
    {
        value: 10,
        iconClass: 'project',
        title: '项目',
        key: 'project'
    }
])

const visitStatsLoading = ref(true)
const visitStatsList = ref<VisitStats[] | null>(Array(3).fill({}))
interface VisitStats {
    title: string
    icon: string
    tagType: 'primary' | 'success' | 'warning'
    growthRate: number
    /** 粒度 */
    granularity: string
    /** 今日数量输出文档  */
    todayCount: number
    totalCount: number
}

/** 格式化增长率 */
const formatGrowthRate = (growthRate: number): string => {
    if (growthRate === 0) {
        return '-'
    }

    const formattedRate = Math.abs(growthRate * 100)
        .toFixed(2)
        .replace(/\.?0+$/, '')
    return formattedRate + '%'
}

/** 获取增长率文本颜色类 */
const getGrowthRateClass = (growthRate: number): string => {
    if (growthRate > 0) {
        return 'color-[--el-color-danger]'
    } else if (growthRate < 0) {
        return 'color-[--el-color-success]'
    } else {
        return 'color-[--el-color-info]'
    }
}

/** 获取访问统计图标 */
const getVisitStatsIcon = (type: string) => {
    switch (type) {
        case 'pv':
            return 'pv'
        case 'uv':
            return 'uv'
        case 'ip':
            return 'ip'
        default:
            return 'pv'
    }
}

onMounted(async () => {
    await getBookNum()
})
</script>
