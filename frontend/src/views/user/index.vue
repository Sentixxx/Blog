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
                                        <el-input v-model="userStore.user.user_instance_name" disabled />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.email')">
                                        <el-input v-model="userStore.user.user_instance_email"
                                            :disabled="editable === false" />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.phone')">
                                        <el-input v-model="userStore.user.user_instance_phone"
                                            :disabled="editable === false" />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.nickname')">
                                        <el-input v-model="userStore.user.user_instance_nickname"
                                            :disabled="editable === false" />
                                    </el-form-item>
                                    <el-form-item :label="$t('user.gender')">
                                        <el-input v-model="userStore.user.user_instance_gender"
                                            :disabled="editable === false" />
                                    </el-form-item>
                                </el-form>
                            </el-col>
                        </el-row>
                    </el-col>
                </el-row>
                <div class="btn">
                    <el-button type="primary" @click="editable = true" v-if="editable === false">{{
                        t('user.edit')
                        }}</el-button>
                    <el-button type="primary" @click="onSave" v-else>{{
                        t('user.save')
                        }}</el-button>
                    <el-button type="primary">{{ t('user.back') }}</el-button>
                    <el-button type="primary">{{ t('user.edit_pass') }}</el-button>
                    <!-- {{ editable }} -->
                </div>
            </el-main>
            <!-- <el-footer>Footer</el-footer> -->
        </el-container>
    </div>
</template>

<script setup lang="ts">
const editable = ref(false)
import { useSettingsStore } from '@/stores'
import { useUserStore } from '@/stores'

const { t } = useI18n()
const settingsStore = useSettingsStore()
const userStore = useUserStore()
const layout = computed(() => settingsStore.layout)

async function onSave() {
    console.log('onSave')
    const res = await userStore.updateUserInfo()
    editable.value = false
}
</script>

<style>
.btn {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
</style>
