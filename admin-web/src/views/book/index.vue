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
                            src="row.book_pic"
                            fit="cover"
                            :preview-src-list="[row.book_pic]"
                            preview-teleported
                        />
                    </template>
                </el-table-column>
                <el-table-column prop="book_name" label="Name" />
                <el-table-column prop="book_author" label="Author" />
                <el-table-column prop="book_isbn_code" label="ISBN" />
                <el-table-column prop="book_cur_stock_num" label="Stock" />
            </el-table>
        </div>
        <el-image src="../../assets/images/404_cloud.png" fit="cover" />
    </div>
</template>

<script setup lang="ts">
import { Search } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
const settingsStore = useSettingsStore()
const layout = computed(() => settingsStore.layout)
const input = ref('')

const select = ref('1')
const tableData = [
    {
        book_id: '1',
        book_pic: '../../assets/images/404.png',
        book_name: 'The Da Vinci Code',
        book_author: 'Dan Brown',
        book_isbn_code: '9787543639131',
        book_cur_stock_num: '10'
    }
]
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
