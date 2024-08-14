<template>
    <div id="book">
        <div class="search-container">
            <el-input v-model="input" style="width: 100%" :placeholder="$t('book.please_input')"
                class="input-with-select" size="large" @keyup.enter="handleSearch">
                <template #prepend>
                    <el-select v-model="select" placeholder="Select" style="width: 115px" size="large">
                        <el-option :label="$t('user.name')" value="user_instance_name" />
                        <el-option :label="$t('user.nickname')" value="user_instance_nickname" />
                        <el-option :label="$t('user.email')" value="user_instance_email" />
                        <el-option :label="$t('user.phone')" value="user_instance_phone" />
                        <el-option :label="$t('user.status')" value="user_instance_status" />
                        <el-option :label="$t('user.group_name')" value="user_instance_group_name" />
                    </el-select>
                </template>
                <template #append>
                    <el-button :icon="Search" @click="handleSearch" />
                </template>
            </el-input>
        </div>
        <div class="show-container">
            <el-table :data="tableData">
                <el-table-column prop="user_instance_name" :label="$t('user.name')" />
                <el-table-column prop="user_instance_nickname" :label="$t('user.nickname')" />
                <el-table-column prop="user_instance_email" :label="$t('user.email')" />
                <el-table-column prop="user_instance_phone" :label="$t('user.phone')" />
                <el-table-column prop="user_instance_status" :label="$t('user.status')">
                    <template #default="scope">
                        <span>{{ statusText(scope.row.user_instance_status) }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="user_instance_group_name" :label="$t('user.group_name')" />
                <el-table-column prop="Edit" :label="$t('book.edit.name')">
                    <template #default="{ row }">
                        <div class="edit_btn">
                            <el-tooltip :content="$t('book.edit.borrow_info')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Search" circle
                                    @click="handleInfoClick(row.user_instance_id)" />
                            </el-tooltip>
                            <el-tooltip :content="$t('book.edit.ban')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Delete" circle
                                    @click="handleBanClick(row.user_instance_id)" />
                            </el-tooltip>

                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <div class="flex justify-center">
                <el-pagination background layout="prev, pager, next" :total="state.total"
                    @current-change="handleCurrentChange" @size-change="handleSizeChange" />
            </div>
        </div>
        <div class="borrow-info-container">
            <el-dialog v-model="borrowInfoVisible" width="1000px">
                <borrow-info-table :data="borrowData" />
            </el-dialog>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Delete, Edit, Search, Ticket } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'
import UserAPI, { UserInfo } from '@/api/user'
import BorrowAPI, { BorrowLog } from '@/api/borrow'
import { SCOPE } from 'element-plus'
import router from '@/router'
const { t } = useI18n()
const settingsStore = useSettingsStore()
const userStore = useUserStore()
const input = ref('')

function statusText(status: number) {
    return status === 1 ? t('user.normal') : t('user.freeze')
}

const allTableData = ref<any[]>([])
const state = reactive({
    page: 1,
    limit: 10,
    total: allTableData.value.length
})

const tableData = computed(() => {
    const start = (state.page - 1) * state.limit
    const end = state.page * state.limit
    return allTableData.value.slice(start, end)
})

const select = ref('user_instance_name')
async function handleSearch() {
    try {
        const params = { [select.value]: input.value }
        const res = await UserAPI.search(params)
        allTableData.value = res
    } catch (error) {
        console.error(error)
    }
}

function handleCurrentChange(val: number) {
    state.page = val
}

function handleSizeChange(val: number) {
    state.limit = val
}

async function initTable() {
    try {
        const res = await UserAPI.getAll()
        allTableData.value = res
        console.log(state.total)
    } catch (error) {
        console.error(error)
    }
}

const borrowData = ref<BorrowLog[]>([])
const borrowInfoVisible = ref<boolean>(false)
async function handleInfoClick(id: number) {
    try {
        const res = await BorrowAPI.getByUserId(id)
        borrowData.value = res
        console.log(borrowData.value)
        borrowInfoVisible.value = true
    } catch (error) {
        console.error(error)
    }
}

const userData = ref<UserInfo>()
async function handleBanClick(id: number) {
    try {
        await UserAPI.banUser(id)
        location.reload()
    } catch (error) {
        console.error(error)
    }
}

watchEffect(() => {
    state.total = allTableData.value.length
})

onMounted(() => {
    initTable()
})
</script>

<style scoped>
.search-container {
    width: calc(80%);
    margin-top: 40px;
    margin-left: auto;
    margin-right: auto;
    padding: 0 0 0 0;
    border: 0 0 0 0;
}

.search-container {
    border: 40 40 40 40x;
}

.time-container {
    text-align: center;
    margin-bottom: 16px;
}
</style>
