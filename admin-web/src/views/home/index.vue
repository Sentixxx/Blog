<template>
    <div class="home-container">
        <el-card shadow="never">
            <el-row justify="space-between">
                <el-col :span="18" :xs="24">
                    <div class="flex h-full items-center">
                        <img class="w-20 h-20 mr-5 rounded-full"
                            :src="userStore.user.user_instance_avatar + '?imageView2/1/w/80/h/80'" />
                        <div>
                            <p>{{ t('system.welcome') + ', ' + userStore.user.user_instance_name }}</p>
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
                            <span class="text-[var(--el-text-color-secondary)]">{{ t('home.booknum') }}</span>
                            <!-- <el-tag type="success" size="small">-</el-tag> -->
                        </div>
                    </template>

                    <div class="flex-x-between mt-2">
                        <span class="text-lg"> {{ booknum }}</span>
                        <svg-icon icon-class="books" size="2em" />
                    </div>
                    <div class="flex-x-between mt-2 text-sm text-[var(--el-text-color-secondary)]">
                        <span>{{ t('home.totalbooknum') }} </span>
                        <span> {{ totalbooknum }}</span>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
                <el-card shadow="never">
                    <template #header>
                        <div class="flex-x-between">
                            <span class="text-[var(--el-text-color-secondary)]">{{ t('home.curBorrowNum') }} </span>
                            <!-- <el-tag type="success" size="small">-</el-tag> -->
                        </div>
                    </template>

                    <div class="flex-x-between mt-2">
                        <span class="text-lg"> {{ curBorrowNum }}</span>
                        <svg-icon icon-class="borrow" size="2em" />
                    </div>
                    <div class="flex-x-between mt-2 text-sm text-[var(--el-text-color-secondary)]">
                        <span> {{ t('home.totalBorrowNum') }} </span>
                        <span> {{ totalBorrowNum }}</span>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
                <el-card shadow="never">
                    <template #header>
                        <div class="flex-x-between">
                            <span class="text-[var(--e-text-color-secondary)]">{{ t('home.curReadTime') }}</span>
                            <!-- <el-tag type="success" size="small">-</el-tag> -->
                        </div>
                    </template>

                    <div class="flex-x-between mt-2">
                        <span class="text-lg"> {{ curReadTime }}</span>
                        <svg-icon icon-class="clock" size="2em" />
                    </div>
                    <div class="flex-x-between mt-2 text-sm text-[var(--el-text-color-secondary)]">
                        <span> {{ t('home.avgReadTime') }} </span>
                        <span> {{ avgReadTime }} </span>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
                <el-card shadow="never">
                    <template #header>
                        <div class="flex-x-between">
                            <span class="text-[var(--el-text-color-secondary)]">{{ t('home.credit') }}</span>
                        </div>
                    </template>

                    <div class="flex-x-between mt-2">
                        <span class="text-lg" v-if="overdueNum > 3"> {{ t('home.bad') }} </span>
                        <span class="text-lg" v-else-if="overdueNum >= 1"> {{ t('home.normal') }} </span>
                        <span class="text-lg" v-else> {{ t('home.good') }} </span>
                        <svg-icon icon-class="bad" size="2em" v-if="overdueNum > 3" />

                        <svg-icon icon-class="ok" size="2em" v-else-if="overdueNum >= 1" />
                        <svg-icon icon-class="good" size="2em" v-else />
                    </div>
                    <div class="flex-x-between mt-2 text-sm text-[var(--el-text-color-secondary)]">
                        <span> {{ t('home.overdueNum') }} </span>
                        <span> {{ overdueNum }}</span>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="10" class="mt-5">
            <el-col :xs="24" :span="16">
                <el-card>
                    <template #header>
                        <div class="flex-x-between">
                            <div class="flex-y-center">{{ t('home.your_book_preference') }}</div>
                            <el-radio-group v-model="dataRange" size="small" @change="handleDateRangeChange">
                                <el-radio-button :label="t('home.recent7days')" :value="1" />
                                <el-radio-button :label="t('home.recent30days')" :value="2" />
                            </el-radio-group>
                        </div>
                    </template>
                </el-card>
            </el-col>
            <el-col :xs="24" :span="8">
                <el-card>
                    <template #header>
                        <div class="flex-x-between">
                            <div class="flex-y-center">
                                {{ t('home.notice') }}
                                <el-icon class="ml-1">
                                    <Notification />
                                </el-icon>
                            </div>
                            <el-link type="primary">
                                <span class="text-xs">{{ t('home.more') }}</span>
                                <el-icon class="text-xs">
                                    <ArrowRight />
                                </el-icon>
                            </el-link>
                        </div>
                    </template>

                    <el-scrollbar height="400px">
                        <div v-for="(item, index) in notices" :key="index" class="flex-y-center py-3">
                            <el-tag :type="getNoticeLevelTag(item.level)" size="small">
                                {{ getNoticeLabel(item.type) }}
                            </el-tag>
                            <el-text truncated class="!mx-2 flex-1 !text-xs !text-[var(--el-text-color-secondary)]">
                                {{ item.title }}
                            </el-text>
                            <el-link>
                                <el-icon class="text-sm">
                                    <View />
                                </el-icon>
                            </el-link>
                        </div>
                    </el-scrollbar>
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
import AuthAPI from '@/api/auth'

const curBorrowNum = ref(0)
const totalBorrowNum = ref(0)
const curReadTime = ref(0)
const avgReadTime = ref(0)
const overdueNum = ref(0)

const setChartOptions = (data: any) => {
    const option = {
        legend: {
            data: data,
            right: '10%',
            top: '30%',
            orient: 'vertical'
        },
        series: [
            {
                type: 'pie',
                stillshowZeroSum: false,
                label: {
                    show: false
                },
                data: data
            }
        ]
    }
    return option
}

const userStore = useUserStore()

const date: Date = new Date()

function getUserNickname() {
    if (userStore.user.user_instance_nickname == null) return userStore.user.user_instance_name
    return userStore.user.user_instance_nickname
}

const { t } = useI18n()

const booknum = ref(0)

const totalbooknum = ref(0)

async function updateInfo() {

    const res = await BookInstanceAPI.getAll()

    totalbooknum.value = res.length
    const bookRes = await BookAPI.getAll()

    for (let i = 0; i < bookRes.length; i++) {
        booknum.value += bookRes[i]?.book_cur_stock_num ?? 0
    }

    if (!localStorage.getItem('TOKEN_KEY')) {
        return
    }

    const borrowRes = await AuthAPI.getUserBorrowInfo()
    curBorrowNum.value = borrowRes.borrow_cnt
    totalBorrowNum.value = borrowRes.current_borrow_cnt
    curReadTime.value = borrowRes.read_time
    overdueNum.value = borrowRes.overdue
    avgReadTime.value = borrowRes.avg_read_time
    console.log(borrowRes)
}

onMounted(async () => {
    await updateInfo()
})
</script>
