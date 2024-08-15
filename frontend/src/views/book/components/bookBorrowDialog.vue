<template>
    <el-dialog v-model="visible" width="800">
        <el-table :data="data">
            <el-table-column type="index" label="ID" width="50" />
            <el-table-column prop="book_instance_id" :label="$t('book.book_instance_id')" />
            <el-table-column prop="book_instance_location" :label="$t('book.location')" />
            <el-table-column :label="$t('book.edit.name')">
                <template #default="{ row }">
                    <div class="btn">
                        <el-button type="primary" size="small" @click="handleBorrowOpen(row.book_instance_id)">
                            {{ $t('book.borrow') }}
                        </el-button>
                        <div v-if="isAdmin()">
                            <el-button type="primary" size="small" @click="handleHistoryOpen(row.book_instance_id)">
                                {{ $t('book.history') }}
                            </el-button>
                            <el-button type="primary" size="small" @click="handleInstanceDelete(row.book_instance_id)">
                                {{ $t('book.edit.delete') }}
                            </el-button>
                            <el-button type="primary" size="small" @click="handleInstanceEdit(row.book_instance_id)">
                                {{ $t('book.edit.name') }}
                            </el-button>
                        </div>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-dialog>
    <el-dialog v-model="innerVisible2" width="500" append-to-body center>
        <div class="his-container">
            <h1>{{ $t('book.history') }}</h1>
            <el-table :data="historyData">
                <el-table-column type="index" label="ID" width="50" />
                <el-table-column prop="user_instance_name" :label="$t('user.name')" />
                <el-table-column prop="borrow_time" :label="$t('book.borrow_time')" />
                <el-table-column prop="actual_return_time" :label="$t('book.return_time')" />
            </el-table>
            <div class="flex justify-center">
                <el-pagination background layout="prev, pager, next" :total="state.total"
                    @current-change="handleCurrentChange" @size-change="handleSizeChange" />
            </div>
        </div>
    </el-dialog>
    <el-dialog v-model="innerVisible" width="500" append-to-body center>
        <div class="time-container">
            <h1>{{ $t('book.return_time') }}</h1>
            <el-date-picker type="datetime" :placeholder="$t('book.return_time')" v-model="return_time" />
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
    <el-dialog v-model="innerVisible3" width="500" append-to-body center>
        <div class="location-container">
            <h1>{{ $t('book.location') }}</h1>
            <el-input :placeholder="$t('book.location')" v-model="Location" />
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="innerVisible3 = false">
                    {{ $t('system.cancel') }}
                </el-button>
                <el-button type="primary" @click="handleLocationConfirm">
                    {{ $t('system.confirm') }}
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { BookInfo } from '@/api/book'
import BookInstanceAPI, { BookInstance } from '@/api/bookInstance'
import BorrowAPI from '@/api/borrow'
import { useUserStore } from '@/stores';
import { isAdmin } from '@/utils/perm'

const userId = defineModel<number>('userId')
const visible = defineModel<boolean>('visible')
const data = defineModel<BookInfo[]>('data')

const return_time = ref<string>('')

const innerVisible = ref<boolean>(false)
const innerVisible2 = ref<boolean>(false)
const innerVisible3 = ref<boolean>(false)
const curBookInstanceId = ref<string>('')
const historyData = ref<any[]>([])

const state = reactive({
    page: 1,
    limit: 10,
    total: historyData.value.length
})

function handleCurrentChange(val: number) {
    state.page = val
}
function handleSizeChange(val: number) {
    state.limit = val
}
const curBookInstance = ref<BookInstance>() as any
async function handleInstanceEdit(id: string) {
    curBookInstanceId.value = id
    curBookInstance.value = await BookInstanceAPI.get(id)
    Location.value = curBookInstance.value.book_instance_location
    innerVisible3.value = true
}

const Location = ref<string>('')
async function handleLocationConfirm() {
    curBookInstance.value.book_instance_location = Location.value
    await BookInstanceAPI.update(curBookInstanceId.value, curBookInstance.value)
    innerVisible3.value = false
    location.reload()
}

async function handleHistoryOpen(id: string) {
    const res = await BorrowAPI.getByBookInstanceId(id)
    historyData.value = res
    innerVisible2.value = true
    curBookInstanceId.value = id
}

async function handleInstanceDelete(id: string) {
    await BookInstanceAPI.delete(id)
    location.reload()
}

function handleBorrowOpen(id: string) {
    return_time.value = ''
    innerVisible.value = true
    curBookInstanceId.value = id
}

async function handleBorrowConfirm() {
    try {
        await BookInstanceAPI.borrow(
            curBookInstanceId.value,
            useUserStore().user.user_instance_id,
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

<style scoped>
.location-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.btn {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.time-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
