<template>
    <div id="borrow">
        <div class="search-container">
            <el-input v-model="input" style="width: 100%" :placeholder="$t('book.please_input')"
                class="input-with-select" size="large" @keyup.enter="handleSearch">
                <template #prepend>
                    <el-select v-model="select" placeholder="Select" style="width: 115px" size="large">
                        <el-option :label="$t('book.name')" value="book_name" />
                        <el-option :label="$t('book.code')" value="book_instance_id" />
                    </el-select>
                </template>
                <template #append>
                    <el-button :icon="Search" @click="handleSearch" />
                </template>
            </el-input>
        </div>
        <div class="show-container">
            <el-table :data="tableData" row-key="return_time"
                :default-sort="{ prop: 'is_completed', order: 'descending' }">
                <el-table-column prop="" :label="$t('book.cover')">
                    <template #default="{ row }">
                        <el-image v-if="row.book_pic" :src="row.book_pic" fit="cover" :preview-src-list="[row.book_pic]"
                            preview-teleported />
                        <el-image v-else src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                            fit="cover" :preview-src-list="[row.book_pic]" preview-teleported />
                    </template>
                </el-table-column>
                <el-table-column prop="book_name" :label="$t('book.name')" />
                <el-table-column prop="book_instance_id" :label="$t('book.code')" />
                <el-table-column prop="borrow_time" :label="$t('book.borrow_time')" />
                <el-table-column prop="return_time" :label="$t('book.return_time')" />
                <el-table-column prop="is_completed" :label="$t('book.is_complete_status')" :filters="[
                    { text: $t('book.not_complete'), value: $t('book.not_complete') },
                    { text: $t('book.is_complete'), value: $t('book.is_complete') }
                ]" :filter-method="filterHandler" />
                <el-table-column prop="Edit" :label="$t('book.edit.name')">
                    <template #default="{ row }">
                        <div class="edit_btn" v-if="row.is_completed == $t('book.not_complete')">
                            <el-tooltip :content="$t('book.edit.delay')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Clock" circle
                                    @click="handleDelayClick(row.borrow_id)" />
                            </el-tooltip>

                            <!-- Return Book Tooltip with Popconfirm -->
                            <el-tooltip :content="$t('book.edit.return')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Ticket" @click="
                                    handleReturnConfirm(row.borrow_id, row.book_instance_id)
                                    " circle />
                            </el-tooltip>
                        </div>
                    </template>
                </el-table-column>
            </el-table>

            <!-- Pagination Component -->
            <div class="flex justify-center">
                <el-pagination background layout="prev, pager, next" :total="state.total"
                    @current-change="handleCurrentChange" @size-change="handleSizeChange" />
            </div>
        </div>
        <div>
            <BorrowDelayDialog v-model:visible="borrowDelayVisible" :data="borrowDelayData" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { Clock, Ticket, Search } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores'
import type { TableColumnCtx } from 'element-plus'
import BookInstanceAPI from '@/api/bookInstance'
import BorrowAPI, { BorrowLog } from '@/api/borrow'
const { t } = useI18n()
const userStore = useUserStore()
const allTableData = ref<BorrowLog[]>([])
const input = ref('')
const select = ref('book_name')

const state = reactive({
    page: 1,
    limit: 10,
    total: allTableData.value.length
})

const tableData = computed(() => {
    const start = (state.page - 1) * state.limit
    const end = state.page * state.limit
    return allTableData.value.slice(start, end).map((row) => ({
        ...row,
        return_time: row.extra_return_time ?? row.should_return_time,
        is_completed: row.is_completed === 1 ? t('book.is_complete') : t('book.not_complete')
    }))
})
function handleCurrentChange(val: number) {
    state.page = val
}

function handleSizeChange(val: number) {
    state.limit = val
}

async function initTable() {
    try {
        const res = await BorrowAPI.getByUserId(userStore.user.user_instance_id)
        allTableData.value = res
        console.log(state.total)
    } catch (error) {
        console.error(error)
    }
}

const filterHandler = (value: string, row: BorrowLog, column: TableColumnCtx<BorrowLog>) => {
    const property = column.property as keyof BorrowLog
    if (property in row) {
        return row[property] === value
    }
    return false
}

async function handleSearch() {
    try {
        const res = await BorrowAPI.search(select.value, input.value)
        allTableData.value = res
    } catch (error) {
        console.error(error)
    }
}

watchEffect(() => {
    state.total = allTableData.value.length
})

onMounted(async () => {
    initTable()
})

const borrowDelayVisible = ref(false)
const borrowDelayData = ref<BorrowLog>()
function handleDelayClick(borrow_id: number) {
    const data = allTableData.value.find((item) => item.borrow_id === borrow_id)
    borrowDelayData.value = data
    borrowDelayVisible.value = true
}

async function handleReturnConfirm(borrow_id: number, book_instance_id: string) {
    try {
        await BookInstanceAPI.returnBookInstance(borrow_id, book_instance_id)
        location.reload()
    } catch (error) {
        console.error(error)
    }
}
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

.book-info-dialog {
    padding: 20px;
}

.book-cover {
    text-align: center;
}

.book-cover .el-image {
    max-width: 100%;
    height: auto;
}

.book-introduction {
    padding-left: 20px;
}

.book-introduction h1,
.book-introduction h2,
.book-introduction h3 {
    margin: 5px 0;
}

.book-introduction p {
    margin: 10px 0;
    color: #606266;
    line-height: 1.6;
}

.time-container {
    text-align: center;
    margin-bottom: 16px;
}
</style>
