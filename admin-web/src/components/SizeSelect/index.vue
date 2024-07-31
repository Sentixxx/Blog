<template>
    <el-dropdown trigger="click" @command="handleSizeChange">
        <div>
            <svg-icon icon-class="size" />
        </div>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item
                    v-for="item of sizeOptions"
                    :key="item.value"
                    :disabled="appStore.size == item.value"
                    :command="item.value"
                >
                    {{ item.label }}
                </el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>
</template>

<script setup lang="ts">
import { SizeEnum } from '@/enums/sizeEnum'
import { useAppStore } from '@/stores/modules/app'

const { t } = useI18n()
const sizeOptions = computed(() => {
    return [
        { label: t('navbar.sizeSelect.default'), value: SizeEnum.DEFAULT },
        { label: t('navbar.sizeSelect.large'), value: SizeEnum.LARGE },
        { label: t('navbar.sizeSelect.small'), value: SizeEnum.SMALL }
    ]
})

const appStore = useAppStore()
function handleSizeChange(size: string) {
    appStore.setSize(size)
    ElMessage.success(t('sizeSelect.message.success'))
}
</script>
