<template>
    <el-table
        :data="tableData"
        row-key="return_time"
        :default-sort="{ prop: 'is_completed', order: 'descending' }"
    >
        <el-table-column prop="" :label="$t('book.cover')">
            <template #default="{ row }">
                <el-image
                    v-if="row.book_pic"
                    :src="row.book_pic"
                    fit="cover"
                    :preview-src-list="[row.book_pic]"
                    preview-teleported
                />
                <el-image
                    v-else
                    src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
                    fit="cover"
                    :preview-src-list="[row.book_pic]"
                    preview-teleported
                />
            </template>
        </el-table-column>
        <el-table-column prop="book_name" :label="$t('book.name')" />
        <el-table-column prop="book_instance_id" :label="$t('book.code')" />
        <el-table-column prop="borrow_time" :label="$t('book.borrow_time')" />
        <el-table-column prop="return_time" :label="$t('book.return_time')" />
        <el-table-column
            prop="is_completed"
            :label="$t('book.is_complete_status')"
            :filters="[
                { text: $t('book.not_complete'), value: $t('book.not_complete') },
                { text: $t('book.is_complete'), value: $t('book.is_complete') }
            ]"
            :filter-method="filterHandler"
        />
    </el-table>
</template>

<script lang="ts" setup>
import { BorrowLog } from '@/api/borrow'
import { TableColumnCtx } from 'element-plus'

const data = defineModel<BorrowLog[]>('data') as any

const { t } = useI18n()

const state = reactive({
    page: 1,
    limit: 10,
    total: data.value.length
})

const tableData = computed(() => {
    const start = (state.page - 1) * state.limit
    const end = state.page * state.limit
    return data.value.slice(start, end).map((row: any) => ({
        ...row,
        return_time: row.extra_return_time ?? row.should_return_time,
        is_completed: row.is_completed === 1 ? t('book.is_complete') : t('book.not_complete')
    }))
})

function handleCurrentChange(val: number) {
    state.page = val
}

function handleSizeChange(val: number) {
    state.limit = val
}

const filterHandler = (value: string, row: BorrowLog, column: TableColumnCtx<BorrowLog>) => {
    const property = column.property as keyof BorrowLog
    if (property in row) {
        return row[property] === value
    }
    return false
}
</script>
