<template>
    <div class="user-container">
        <el-container>
            <el-header>Header</el-header>
            <el-main>
                <el-row>
                    <el-col :span="24">
                        <el-row>
                            <el-col :span="24">
                                <el-form :model="userStore.user" label-width="80px">
                                    <el-form-item :label="$t('user.name')">
                                        <el-input
                                            v-model="userStore.user.user_instance_name"
                                            disabled
                                        />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.email')">
                                        <el-input
                                            v-model="userStore.user.user_instance_email"
                                            disabled
                                        />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.mobile')">
                                        <el-input
                                            v-model="userStore.user.user_instance_mobile"
                                            disabled
                                        />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.nickname')">
                                        <el-input
                                            v-model="userStore.user.user_instance_nickname"
                                            disabled
                                        />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.gender')">
                                        <el-input
                                            v-model="userStore.user.user_instance_gender"
                                            disabled
                                        />
                                    </el-form-item>
                                </el-form>
                            </el-col>
                        </el-row>
                    </el-col>
                </el-row>
                <el-button type="primary">{{ $t('user.edit') }}</el-button>
                <el-button type="primary">{{ $t('user.back') }}</el-button>
                <el-button type="primary">{{ $t('user.edit_pass') }}</el-button>
            </el-main>
            <el-footer>Footer</el-footer>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'

const { t } = useI18n()
const settingsStore = useSettingsStore()
const userStore = useUserStore()
const layout = computed(() => settingsStore.layout)
</script>
