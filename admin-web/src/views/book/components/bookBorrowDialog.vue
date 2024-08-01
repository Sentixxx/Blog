<template>
    <el-dialog v-model="visible" width="800">
        <el-table :data="data">
            <el-table-column type="index" label="ID" width="50" />
            <el-table-column prop="book_instance_id" :label="$t('book.book_instance_id')" />
            <el-table-column prop="book_instance_location" :label="$t('book.location')" />
            <el-table-column label="Borrow">
                <template #default="{ row }">
                    <el-button type="primary" @click="handleBorrowOpen(row.book_instance_id)">
                        {{ $t('book.borrow') }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-dialog>
    <el-dialog v-model="innerVisible" width="500" append-to-body center>
        <div class="time-container">
            <h1>{{ $t('book.return_time') }}</h1>
            <el-date-picker
                type="datetime"
                :placeholder="$t('book.return_time')"
                v-model="return_time"
            />
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="innerVisible = false">
                    {{ $t('system.cancel') }}
                </el-button>
                <el-button type="primary" @click="handleBorrowConfirm">
                    {{ $t('system.confirm') }}
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { BookInfo } from '@/api/book'
import BookInstanceAPI from '@/api/bookInstance'

const userId = defineModel<number>('userId')
const visible = defineModel<boolean>('visible')
const data = defineModel<BookInfo[]>('data')

const return_time = ref<string>('')

const innerVisible = ref<boolean>(false)
const curBookInstanceId = ref<string>('')

function handleBorrowOpen(id: string) {
    return_time.value = ''
    innerVisible.value = true
    curBookInstanceId.value = id
}

async function handleBorrowConfirm() {
    try {
        await BookInstanceAPI.borrow(
            curBookInstanceId.value,
            userId.value as number,
            return_time.value,
            data.value?.[0].book_id ?? 0
        )
        innerVisible.value = false
        location.reload()
    } catch (e) {
        // ElMessage.error()
        console.error(e)
    }
}
</script>
