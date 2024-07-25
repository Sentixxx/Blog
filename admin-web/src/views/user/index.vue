<template>
    <div class="book-container">book</div>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores'
const settingsStore = useSettingsStore()
const layout = computed(() => settingsStore.layout)
</script>
