<template>
    <div id="book">
        <div class="search-container">
            <el-input
                v-model="input"
                style="width: 100%"
                :placeholder="$t('book.please_input')"
                class="input-with-select"
                size="large"
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
                <el-table-column type="index" label="No" width="50" />
                <el-table-column prop="" label="Cover">
                    <template #default="{ row }">
                        <el-image
                            :src="row.book_pic"
                            fit="cover"
                            :preview-src-list="[row.book_pic]"
                            preview-teleported
                        />
                    </template>
                </el-table-column>
                <el-table-column prop="book_name" label="Name" />
                <el-table-column prop="book_author" label="Author" />
                <el-table-column prop="book_introduce" label="introduce" />
                <el-table-column prop="Edit" label="edit">
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
                                @click="handleInfoClick"
                            ></el-button>
                        </el-tooltip>
                        <el-tooltip
                            :content="$t('book.edit.edit')"
                            effect="dark"
                            placement="bottom"
                        >
                            <el-button type="primary" :icon="Edit" circle></el-button>
                        </el-tooltip>
                        <el-tooltip
                            :content="$t('book.edit.delete')"
                            effect="dark"
                            placement="bottom"
                        >
                            <el-button type="primary" :icon="Delete" circle></el-button>
                        </el-tooltip>
                        <el-tooltip
                            :content="$t('book.edit.borrow')"
                            effect="dark"
                            placement="bottom"
                        >
                            <el-button type="primary" :icon="Ticket" circle></el-button>
                        </el-tooltip>
                    </div>
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
            <el-dialog v-model="bookInfoVisible" width="800">
                <el-image :src="currentData.book_pic" fit="cover" />
            </el-dialog>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Delete, Edit, Search, Ticket } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
import request from '@/utils/request'
import { useUserStore } from '@/stores'
import { info } from 'console'
const { t } = useI18n()
const settingsStore = useSettingsStore()
const userStore = useUserStore()

const layout = computed(() => settingsStore.layout)
const input = ref('')
let bookInfoVisible = ref(false)

const select = ref('book_name')
let allTableData: Array<any> = [
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    }
]

const state = reactive({
    page: 1,
    limit: 10,
    total: allTableData.length
})

const currentData = reactive({
    book_id: '1',
    book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
    book_name: 'The Da Vinci Code',
    book_author: 'Dan Brown',
    book_introduce: '这是一个',
    book_cur_stock_num: '10'
})
const tableData = computed(() => {
    return allTableData.filter(
        (item, index) => index < state.page * state.limit && index >= (state.page - 1) * state.limit
    )
})

async function handleSearch() {
    try {
        const res = await request({
            url: '/book/search',
            method: 'get',
            params: {
                [select.value]: input.value
            }
        })
        console.log(res)
        allTableData = res.data
    } catch (error) {
        console.error(error)
    }
}

function handleCurrentChange(val: number) {
    state.page = val
}

function handleInfoClick() {
    bookInfoVisible.value = true
}

function handleSizeChange(val: number) {
    state.limit = val
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
</style>
