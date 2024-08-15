<template>
    <div id="book">
        <div class="search-container">
            <div class="input-container">
                <el-input v-model="input" style="width: 100%" :placeholder="$t('book.please_input')"
                    class="input-with-select" size="large" @keyup.enter="handleSearch">
                    <template #prepend>
                        <el-select v-model="select" placeholder="Select" style="width: 115px" size="large">
                            <el-option :label="$t('book.name')" value="book_name" />
                            <el-option :label="$t('book.isbn')" value="book_isbn_code" />
                            <el-option :label="$t('book.author')" value="book_author" />
                        </el-select>
                    </template>
                    <template #append>
                        <el-button :icon="Search" @click="handleSearch" round />
                    </template>
                </el-input>
            </div>
            <div>
                <el-button type="info" :icon="Plus" @click="addBookInfoVisible = true" />
            </div>
        </div>
        <div class="show-container">
            <el-table :data="tableData">
                <el-table-column prop="" :label="$t('book.cover')">
                    <template #default="{ row }">
                        <el-image :src="row.book_pic" fit="cover" :preview-src-list="[row.book_pic]" preview-teleported
                            v-if="row.book_pic" />
                        <el-image src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                            fit="cover" :preview-src-list="[row.book_pic]" preview-teleported v-else />
                    </template>
                </el-table-column>
                <el-table-column prop="book_name" :label="$t('book.name')" />
                <el-table-column prop="book_author" :label="$t('book.author')" />
                <el-table-column prop="book_introduce" :label="$t('book.introduce')" />
                <el-table-column prop="Edit" :label="$t('book.edit.name')">
                    <template #default="{ row }">
                        <div class="edit_btn">
                            <el-tooltip :content="$t('book.edit.info')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Search" circle @click="handleInfoClick(row.book_id)" />
                            </el-tooltip>
                            <el-tooltip :content="$t('book.edit.name')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Edit" circle @click="handleEditClick(row.book_id)" />
                            </el-tooltip>
                            <el-tooltip :content="$t('book.edit.delete')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Delete" @click="handleDeleteConfirm(row.book_id)"
                                    circle />
                            </el-tooltip>

                            <el-tooltip :content="$t('book.edit.add')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="Plus" circle @click="handleAddClick(row.book_id)" />
                            </el-tooltip>
                            <el-tooltip :content="$t('book.edit.show')" effect="dark" placement="bottom">
                                <el-button type="primary" :icon="List" circle @click="handleShowClick(row.book_id)" />
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
        <div class="book-info-container">
            <book-info-dialog v-model:visible="bookInfoVisible" :data="currentBookData" />
        </div>
        <div class="add-book-info-container">
            <add-book-dialog v-model:visible="addBookInfoVisible" :book_id="curBookId" />
        </div>
        <div class="add-book-instance-container">
            <add-book-instance-dialog v-model:visible="addVisible" :book_id="curBookId" />
        </div>
        <div class="edit-book-info-container">
            <edit-book-dialog v-model:visible="editBookVisible" :data="currentBookData" />
        </div>
        <div class="show-list-container">
            <book-borrow-dialog v-model:visible="showInstanceVisible" :data="bookInstnaceData" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { Delete, Edit, Search, Ticket, Plus, List } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'
import BookAPI, { BookInfo } from '@/api/book'
import BookInstanceAPI from '@/api/bookInstance'
import BorrowAPI from '@/api/borrow'
const { t } = useI18n()
const userStore = useUserStore()
const input = ref('')
const bookInfoVisible = ref(false)
const select = ref('book_name')
const allTableData = ref<any[]>([])
const addBookInfoVisible = ref<boolean>(false)
const currentBookData = ref<BookInfo>({
    book_id: 1,
    book_name: '',
    book_author: '',
    book_introduce: '',
    book_pic: '',
    book_isbn_code: '',
    book_cur_stock_num: 0
})

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
    // console.log('book')
    initTable()
})

const addVisible = ref(false)
const curBookId = ref<any>()
async function handleAddClick(book_id: number) {
    if (userStore.user.user_instance_id === 0) {
        ElMessage.error('Please login first')
    }
    curBookId.value = book_id
    addVisible.value = true
}

const editBookVisible = ref<boolean>(false)
async function handleEditClick(id: number) {
    try {
        const res = await BookAPI.get(id)
        currentBookData.value = res
        console.log(res)
        editBookVisible.value = true
    } catch (error) {
        console.error(error)
    }
}

const showInstanceVisible = ref<boolean>(false)
const bookInstnaceData = ref<any[]>([])
async function handleShowClick(id: number) {
    try {
        const res = await BookInstanceAPI.getById(id)
        bookInstnaceData.value = res
        showInstanceVisible.value = true
    } catch (error) {
        console.error(error)
    }
}

async function handleDeleteConfirm(book_id: number) {
    try {
        await BookAPI.delete(book_id)
        location.reload()
    } catch (e) {
        // ElMessage.error()
        console.error(e)
    }
}
</script>

<style scoped>
.search-container {
    width: calc(80%);
    margin-top: 20px;
    margin-left: auto;
    margin-right: auto;
    padding: 0 0 0 0;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 10px;
    border-color: transparent;
    box-shadow: 0 0 0 0;

    .input-container {
        border: 40 40 40 40px;
        flex-grow: 1;
    }
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
