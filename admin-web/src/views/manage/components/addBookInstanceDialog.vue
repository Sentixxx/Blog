<template>
    <el-dialog v-model="visible">
        <div class="form-container full-w">
            <el-form
                ref="addBookFormRef"
                style="max-width: 600px"
                :model="addBookData"
                :rules="addRules"
                :size="formSize"
                label-width="auto"
                status-icon
            >
                <el-form-item :label="$t('book.location')" prop="book_instance_location">
                    <el-input v-model="addBookData.book_instance_location" />
                </el-form-item>
            </el-form>
        </div>
        <template #footer>
            <el-button @click="visible = false">{{ $t('book.cancel') }}</el-button>
            <el-button type="primary" @click="addBook">{{ $t('book.confirm') }}</el-button>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { BookInstance } from '@/api/bookInstance'
import { ComponentSize, FormInstance, FormRules } from 'element-plus'
import BookInstanceAPI from '@/api/bookInstance'

const { t } = useI18n()

const formSize = ref<ComponentSize>('default')

const visible = defineModel<boolean>('visible')
const book_id = defineModel<number>('book_id')

const addBookFormRef = ref<FormInstance>()

const addBookData = ref<BookInstance>({} as any)

const addRules = reactive<FormRules<BookInstance>>({
    book_instance_location: [{ required: true, message: t('book.require_name'), trigger: 'blur' }]
})

async function addBook() {
    addBookFormRef.value?.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const res = await BookInstanceAPI.add(book_id.value ?? undefined, addBookData.value)
            } catch (error) {
                ElMessage.error(t('book.add_fail'))
                return
            }
            ElMessage.success(t('book.add_success'))
            visible.value = false
            location.reload()
        } else {
            ElMessage.error(t('book.invalid_form'))
        }
    })
}
</script>

<style>
.form-container {
    padding: 20px;
    justify-content: center;
    align-items: center;
}
</style>
