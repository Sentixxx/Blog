<template>
    <div id="book">
        <div class="search-container">
            <el-input
                v-model="input"
                style="width: 100%"
                :placeholder="$t('book.please_input')"
                class="input-with-select"
                size="large"
                @keyup.enter="handleSearch"
            >
                <template #prepend>
                    <el-select
                        v-model="select"
                        placeholder="Select"
                        style="width: 115px"
                        size="large"
                    >
                        <el-option :label="$t('book.name')" value="book_name" />
                        <el-option :label="$t('book.isbn')" value="book_isbn_code" />
                        <el-option :label="$t('book.author')" value="book_author" />
                    </el-select>
                </template>
                <template #append>
                    <el-button :icon="Search" @click="handleSearch" />
                </template>
            </el-input>
        </div>
        <div class="show-container">
            <el-table :data="tableData">
                <el-table-column prop="" :label="$t('book.cover')">
                    <template #default="{ row }">
                        <el-image
                            :src="row.book_pic"
                            fit="cover"
                            :preview-src-list="[row.book_pic]"
                            preview-teleported
                            v-if="row.book_pic"
                        />
                        <el-image
                            src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                            fit="cover"
                            :preview-src-list="[row.book_pic]"
                            preview-teleported
                            v-else
                        />
                    </template>
                </el-table-column>
                <el-table-column prop="book_name" :label="$t('book.name')" />
                <el-table-column prop="book_author" :label="$t('book.author')" />
                <el-table-column prop="book_introduce" :label="$t('book.introduce')" />
                <el-table-column prop="Edit" :label="$t('book.edit.name')">
                    <template #default="{ row }">
                        <div class="edit_btn">
                            <el-tooltip
                                :content="$t('book.edit.info')"
                                effect="dark"
                                placement="bottom"
                            >
                                <el-button
                                    type="primary"
                                    :icon="Search"
                                    circle
                                    @click="handleInfoClick(row.book_id)"
                                />
                            </el-tooltip>
                            <el-tooltip
                                :content="$t('book.edit.borrow')"
                                effect="dark"
                                placement="bottom"
                            >
                                <el-button
                                    type="primary"
                                    :icon="Ticket"
                                    circle
                                    @click="handleBorrowClick(row.book_id)"
                                />
                            </el-tooltip>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
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
        <div class="book-info-container">
            <book-info-dialog v-model:visible="bookInfoVisible" :data="currentBookData" />
        </div>
        <div class="book-borrow-container">
            <book-borrow-dialog
                v-model:visible="borrowListVisible"
                :data="bookInstanceData"
                :userId="userStore.user.user_instance_id"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { Delete, Edit, Search, Ticket } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'
import BookAPI, { BookInfo } from '@/api/book'
import BookInstanceAPI from '@/api/bookInstance'
const { t } = useI18n()
const settingsStore = useSettingsStore()
const userStore = useUserStore()

const layout = computed(() => settingsStore.layout)
const input = ref('')
const bookInfoVisible = ref(false)
const select = ref('book_name')
const allTableData = ref<any[]>([])
const currentBookData = ref<BookInfo>({
    book_id: 1,
    book_name: '',
    book_author: '',
    book_introduce: '',
    book_pic: '',
    book_isbn_code: '',
    book_cur_stock_num: 0
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
    return allTableData.value.slice(start, end)
})

async function handleSearch() {
    try {
        const res = await BookAPI.search(select.value, input.value)
        console.log(res)
        allTableData.value = res
    } catch (error) {
        console.error(error)
    }
}

function handleCurrentChange(val: number) {
    state.page = val
}

async function handleInfoClick(id: number) {
    try {
        const res = await BookAPI.get(id)
        currentBookData.value = res
        bookInfoVisible.value = true
    } catch (error) {
        console.error(error)
    }
}

function handleSizeChange(val: number) {
    state.limit = val
}

async function initTable() {
    try {
        const res = await BookAPI.getAll()
        allTableData.value = res
        console.log(state.total)
    } catch (error) {
        console.error(error)
    }
}

watchEffect(() => {
    state.total = allTableData.value.length
})

onMounted(() => {
    console.log('book')
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
