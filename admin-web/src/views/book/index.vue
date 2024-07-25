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
                <el-table-column prop="name" label="Name"/>
            </el-table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Search } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores'
const settingsStore = useSettingsStore()
const layout = computed(() => settingsStore.layout)
const input = ref('')
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
    border: 40 40 40 40;
}
</style>
