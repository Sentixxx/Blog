<template>
    <div id="borrow">
        <div class="show-container">
            <el-table :data="tableData" row-key="return_time">
                <el-table-column prop="" :label="$t('book.cover')">
                    <template #default="{ row }">
                        <el-image
                            v-if="row.book_pic"
                            :src="row.book_pic"
                            fit="cover"
                            :preview-src-list="[row.book_pic]"
                            preview-teleported
                        />
                        <el-image
                            v-else
                            src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                            fit="cover"
                            :preview-src-list="[row.book_pic]"
                            preview-teleported
                        />
                    </template>
                </el-table-column>
                <el-table-column prop="book_name" :label="$t('book.name')" />
                <el-table-column prop="book_instance_name" :label="$t('book.code')" />
                <el-table-column prop="borrow_time" :label="$t('book.borrow_time')" />
                <el-table-column prop="return_time" :label="$t('book.return_time')" />
                <el-table-column
                    prop="is_completed"
                    :label="$t('book.is_complete')"
                    :filters="[
                        { text: $t('book.not_complete'), value: $t('book.not_complete') },
                        { text: $t('book.is_complete'), value: $t('book.is_complete') }
                    ]"
                    :filter-method="filterHandler"
                />
                <el-table-column prop="Edit" :label="$t('book.edit.name')">
                    <template #default="{ row }">
                        <div class="edit_btn">
                            <!-- Edit Button Tooltip -->
                            <el-tooltip
                                :content="$t('book.edit.name')"
                                effect="dark"
                                placement="bottom"
                            >
                                <el-button type="primary" :icon="Edit" circle />
                            </el-tooltip>

                            <!-- Delete Button Tooltip -->
                            <el-tooltip
                                :content="$t('book.edit.delete')"
                                effect="dark"
                                placement="bottom"
                            >
                                <el-button type="primary" :icon="Delete" circle />
                            </el-tooltip>

                            <!-- Return Book Tooltip with Popconfirm -->

                            <el-popconfirm
                                :title="$t('book.confirm')"
                                @confirm="handleReturnConfirm(row.borrow_id, row.book_instance_id)"
                            >
                                <template #reference>
                                    <div>
                                        <el-tooltip
                                            :content="$t('book.edit.return')"
                                            effect="dark"
                                            placement="bottom"
                                        >
                                            <el-button type="primary" :icon="Ticket" circle />
                                        </el-tooltip>
                                    </div>
                                </template>
                            </el-popconfirm>
                        </div>
                    </template>
                </el-table-column>
            </el-table>

            <!-- Pagination Component -->
            <div class="flex justify-center">
                <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="state.total"
                    @current-change="handleCurrentChange"
                    @size-change="handleSizeChange"
                />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Delete, Edit, Search, Ticket } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'
import type { TableColumnCtx } from 'element-plus'
import BookAPI, { BookInfo } from '@/api/book'
import BookInstanceAPI from '@/api/bookInstance'
import BorrowAPI, { BorrowLog } from '@/api/borrow'
import { get } from 'http'
const { t } = useI18n()
const settingsStore = useSettingsStore()
const userStore = useUserStore()

const layout = computed(() => settingsStore.layout)
const input = ref('')
const bookInfoVisible = ref(false)
const innerBorrowVisible = ref(false)
const curBookInstance = ref<any>()
const time1 = ref('')
const select = ref('book_name')
const allTableData = ref<BorrowLog[]>([])
const currentData = ref<BorrowLog>({
    borrow_id: 0,
    book_name: '?',
    book_instance_id: '0',
    borrow_time: '',
    should_return_time: '',
    extra_return_time: '',
    is_completed: 0
})
const borrowListVisible = ref(false)
const bookInstanceData = ref<any[]>([])
const totalPages = ref(1)

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

function handleReturnTime(row: any) {
    if (row.extra_return_time !== null) {
        return row.value.extra_return_time
    } else {
        return row.should_return_time
    }
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

watchEffect(() => {
    state.total = allTableData.value.length
})

onMounted(async () => {
    initTable()
})

async function handleBorrowClick(book_id: number) {
    console.log(userStore)
    if (userStore.user.user_instance_id === 0) {
        ElMessage.error('Please login first')
    }
    const res = await BookInstanceAPI.getById(book_id)
    bookInstanceData.value = res
    borrowListVisible.value = true
}

async function handleReturnConfirm(borrow_id: number, book_instance_id: string) {
    console.log(time1.value)
    try {
        await BookInstanceAPI.returnBookInstance(borrow_id, book_instance_id)
        innerBorrowVisible.value = false
        borrowListVisible.value = false
    } catch (error) {
        console.error(error)
    }
}

function handleBorrowOpen(id: any) {
    time1.value = ''
    innerBorrowVisible.value = true
    curBookInstance.value = id
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
