<template>
    <el-dialog v-model="visible" width="800" :title="data.book_name">
        <div class="book-info-dialog">
            <el-row>
                <!-- 图书封面 -->
                <el-col :span="8" class="book-cover">
                    <el-image :src="data.book_pic" fit="cover" v-if="data.book_pic" />
                    <el-image
                        src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                        fit="cover"
                        preview-teleported
                        v-else
                    />
                    <div>{{ $t('book.stock') }}: {{ data.book_cur_stock_num }}</div>
                </el-col>

                <!-- 图书简介 -->
                <el-col :span="16" class="book-introduction">
                    <p>{{ data.book_introduce }}</p>
                    <el-divider />
                    <h3>{{ $t('book.author') }}: {{ data.book_author }}</h3>
                    <h3>{{ $t('book.isbn') }}: {{ data.book_isbn_code }}</h3>
                    <h3>{{ $t('book.press') }}: {{ data.book_press }}</h3>
                </el-col>
            </el-row>
        </div>
    </el-dialog>
</template>

<script setup lang="ts">
import { BookInfo } from '@/api/book'

const data = defineModel<BookInfo>('data') as any
const visible = defineModel<boolean>('visible')
</script>

<style>
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
</style>
