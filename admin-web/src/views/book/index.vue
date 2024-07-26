<template>
    <div id="book">
        <div class="search-container">
            <el-input
                v-model="input"
                style="width: 100%"
                placeholder="Please input"
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
                        <el-option label="Bookname" value="1" />
                        <el-option label="ISBN" value="2" />
                        <el-option label="Autor" value="3" />
                    </el-select>
                </template>
                <template #append>
                    <el-button :icon="Search" />
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
                <el-table-column prop="book_cur_stock_num" label="Stock" />
            </el-table>
            <div class="flex justify-center">
                <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="10000"
                    @current-change="handleCurrentChange"
                    @size-change="handleSizeChange"
                />
            </div>
        </div>
        <!-- <el-image :src="require('@/assets/images/404_cloud.png')" fit="cover" /> -->
    </div>
</template>

<script setup lang="ts">
import { Search } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
import { table } from 'console'
const settingsStore = useSettingsStore()
const layout = computed(() => settingsStore.layout)
const input = ref('')

const select = ref('1')
const allTableData = [
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
    {
        book_id: '1',
        book_pic: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_introduce: '这是一个',
        book_cur_stock_num: '10'
    },
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

const tableData = computed(() => {
    return allTableData.filter(
        (item, index) => index < state.page * state.limit && index >= (state.page - 1) * state.limit
    )
})

function handleCurrentChange(val: number) {
    state.page = val
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
