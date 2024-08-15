<template>
    <el-dialog v-model="visible">
        <div class="form-container full-w">
            <el-form ref="editBookFormRef" style="max-width: 600px" :model="editBookData" :rules="editRules"
                :size="formSize" label-width="auto" status-icon>
                <el-form-item :label="$t('book.name')" prop="book_name">
                    <el-input v-model="editBookData.book_name" />
                </el-form-item>

                <el-form-item :label="$t('book.author')" prop="book_author">
                    <el-input v-model="editBookData.book_author" />
                </el-form-item>
                <el-form-item :label="$t('book.isbn')" prop="book_isbn_code">
                    <el-input v-model="editBookData.book_isbn_code" />
                </el-form-item>
                <el-form-item :label="$t('book.press')" prop="book_press">
                    <el-input v-model="editBookData.book_press" />
                </el-form-item>
                <el-form-item :label="$t('book.type')" prop="book_type">
                    <el-input v-model="editBookData.book_type" />
                </el-form-item>
                <el-form-item :label="$t('book.introduce')" prop="book_introduce">
                    <el-input v-model="editBookData.book_introduce" type="textarea" />
                </el-form-item>
            </el-form>
        </div>
        <template #footer>
            <el-button @click="visible = false">{{ $t('book.cancel') }}</el-button>
            <el-button type="primary" @click="editBook">{{ $t('book.confirm') }}</el-button>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { BookInfo } from '@/api/book'
import { ComponentSize, FormInstance, FormRules } from 'element-plus'
import BookAPI from '@/api/book'

const { t } = useI18n()

const formSize = ref<ComponentSize>('default')

const visible = defineModel<boolean>('visible')

const data = defineModel<BookInfo>('data')

const editBookFormRef = ref<FormInstance>()

const editBookData = ref<BookInfo>(data.value as BookInfo)

const editRules = reactive<FormRules<BookInfo>>({
    book_name: [{ required: true, message: t('book.require_name'), trigger: 'blur' }],
    book_introduce: [{ required: true, message: t('book.require_introduce'), trigger: 'blur' }],
    book_author: [{ required: true, message: t('book.require_author'), trigger: 'blur' }],
    book_isbn_code: [{ required: true, message: t('book.require_isbn'), trigger: 'blur' }],
    book_press: [{ required: true, message: t('book.require_press'), trigger: 'blur' }]
})

async function editBook() {
    editBookFormRef.value?.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const book_id = data.value?.book_id ?? -1
                await BookAPI.update(book_id, editBookData.value)
            } catch (error) {
                ElMessage.error(t('book.edit_fail'))
                return
            }
            ElMessage.success(t('book.edit_success'))
            visible.value = false
            location.reload()
        } else {
            ElMessage.error(t('book.invalid_form'))
        }
    })
}

watch(
    data,
    (newData) => {
        editBookData.value = { ...newData } as any
    },
    { immediate: true }
)
</script>

<style>
.form-container {
    padding: 20px;
    justify-content: center;
    align-items: center;
}
</style>
