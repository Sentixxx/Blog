<template>
    <div class="home-container">{{ useUserStore().user.user_instance_name }}</div>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'
const settingsStore = useSettingsStore()
const layout = computed(() => settingsStore.layout)
</script>
