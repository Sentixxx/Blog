<template>
    <el-dialog v-model="visible" width="800">
        <div class="time-container">
            <h1>{{ $t('book.return_time') }}</h1>
            <el-date-picker type="datetime" v-model="new_return_time" />
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="visible = false">
                    {{ $t('system.cancel') }}
                </el-button>
                <el-button type="primary" @click="handleBorrowDelayConfirm">
                    {{ $t('system.confirm') }}
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import BorrowAPI, { BorrowLog } from '@/api/borrow'

const visible = defineModel<boolean>('visible')
const data = defineModel<BorrowLog>('data')

const new_return_time = ref<string>(data.value?.extra_return_time ?? '')

async function handleBorrowDelayConfirm() {
    try {
        await BorrowAPI.delay(data.value?.borrow_id as number, new_return_time.value)
        visible.value = false
        location.reload()
    } catch (e) {
        // ElMessage.error()
        console.error(e)
    }
}

watch(
    data,
    (newData) => {
        new_return_time.value = newData?.extra_return_time ?? newData?.should_return_time ?? ''
    },
    { immediate: true }
)
</script>

<style scoped>
.time-container {
    padding: 20px;
    text-align: center;
}
</style>
