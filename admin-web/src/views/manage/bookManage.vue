<template>
    <div id="book">
        <div class="search-container">
            <div>
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
            <div>
                <el-button type="primary" @click="initTable">{{ $t('book.add') }}</el-button>
            </div>
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
                                :content="$t('book.edit.name')"
                                effect="dark"
                                placement="bottom"
                            >
                                <el-button type="primary" :icon="Edit" circle />
                            </el-tooltip>
                            <el-tooltip
                                :content="$t('book.edit.delete')"
                                effect="dark"
                                placement="bottom"
                            >
                                <el-button type="primary" :icon="Delete" circle />
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
            <el-dialog v-model="bookInfoVisible" width="800" :title="currentBookData.book_name">
                <div class="book-info-dialog">
                    <el-row>
                        <!-- 图书封面 -->
                        <el-col :span="8" class="book-cover">
                            <el-image
                                :src="currentBookData.book_pic"
                                fit="cover"
                                v-if="currentBookData.book_pic"
                            />
                            <el-image
                                src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                                fit="cover"
                                preview-teleported
                                v-else
                            />
                            <div>
                                {{ $t('book.stock') }}: {{ currentBookData.book_cur_stock_num }}
                            </div>
                        </el-col>

                        <!-- 图书简介 -->
                        <el-col :span="16" class="book-introduction">
                            <p>{{ currentBookData.book_introduce }}</p>
                            <el-divider />
                            <h3>{{ $t('book.author') }}: {{ currentBookData.book_author }}</h3>
                            <h3>{{ $t('book.isbn') }}: {{ currentBookData.book_isbn_code }}</h3>
                            <h3>{{ $t('book.press') }}: {{ currentBookData.book_press }}</h3>
                        </el-col>
                    </el-row>
                </div>
            </el-dialog>
        </div>
        <div class="book-borrow-container">
            <el-dialog v-model="borrowListVisible" width="800">
                <el-table :data="bookInstanceData">
                    <el-table-column type="index" label="No" width="50" />
                    <el-table-column prop="book_instance_id" label="ID" />
                    <el-table-column prop="book_instance_location" label="Location" />
                    <el-table-column label="Borrow">
                        <template #default="{ row }">
                            <el-button
                                type="primary"
                                @click="handleBorrowOpen(row.book_instance_id)"
                            >
                                {{ $t('book.borrow') }}
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-dialog>
            <el-dialog v-model="innerBorrowVisible" width="500" append-to-body center>
                <div class="time-container">
                    <h1>{{ $t('book.return_time') }}</h1>
                    <el-date-picker
                        type="datetime"
                        :placeholder="$t('book.return_time')"
                        v-model="time1"
                    />
                </div>
                <template #footer>
                    <div class="dialog-footer">
                        <el-button @click="innerBorrowVisible = false">
                            {{ $t('system.cancel') }}
                        </el-button>
                        <el-button type="primary" @click="handleBorrowConfirm">
                            {{ $t('system.confirm') }}
                        </el-button>
                    </div>
                </template>
            </el-dialog>
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
const innerBorrowVisible = ref(false)
const curBookInstance = ref<any>()
const time1 = ref('')
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

async function handleBorrowConfirm() {
    console.log(time1.value)
    try {
        await BookInstanceAPI.borrow(
            curBookInstance.value,
            userStore.user.user_instance_id,
            time1.value,
            currentBookData.value.book_id
        )
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
