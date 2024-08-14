<template>
    <div class="login-container">
        <!--Top-Tool-Bar-->
        <div class="top-bar">
            <el-switch
                v-model="isDark"
                inline-prompt
                active-icon="Moon"
                inactive-icon="Sunny"
                @change="toggleTheme"
            />
            <lang-select class="ml-2 cursor-pointer" />
        </div>
        <!--Regist-Form-->
        <el-card class="login-card">
            <div class="text-center relative">
                <h2>{{ defaultSettings.title }}</h2>
                <div class="ml-2 absolute-rt">
                    <el-button type="primary" link @click="handlejump">
                        {{ $t('system.jump') }}
                    </el-button>
                </div>
            </div>
            <el-form ref="registFormRef" :model="registData" :rules="loginRules" class="login-form">
                <!--Username-->
                <el-form-item prop="username">
                    <div class="input-wrapper">
                        <i-ep-user class="mx-2" /><el-input
                            ref="username"
                            v-model="registData.username"
                            :placeholder="$t('login.username')"
                            name="username"
                            size="large"
                            class="h-[48px]"
                        />
                    </div>
                </el-form-item>

                <!--Password-->
                <el-tooltip :visible="isCapslock" :content="$t('login.capslock')" placement="right">
                    <el-form-item prop="password">
                        <div class="input-wrapper">
                            <i-ep-lock class="mx-2" />
                            <el-input
                                v-model="registData.password"
                                :placeholder="$t('login.password')"
                                type="password"
                                name="password"
                                @keyup="checkCapslock"
                                @keyup.enter="handleRegistSubmit"
                                size="large"
                                class="h-[48px] pr-2"
                                show-password
                            />
                        </div>
                    </el-form-item>
                </el-tooltip>
                <el-tooltip :visible="isCapslock" :content="$t('login.capslock')" placement="right">
                    <el-form-item prop="password">
                        <div class="input-wrapper">
                            <i-ep-lock class="mx-2" />
                            <el-input
                                v-model="registData.repassword"
                                :placeholder="$t('login.password')"
                                type="password"
                                name="password"
                                @keyup="checkCapslock"
                                @keyup.enter="handleRegistSubmit"
                                size="large"
                                class="h-[48px] pr-2"
                                show-password
                            />
                        </div>
                    </el-form-item>
                </el-tooltip>
                <!-- 验证码 -->
                <el-form-item prop="captchaCode">
                    <div class="input-wrapper">
                        <svg-icon icon-class="captcha" class="mx-2" />
                        <el-input
                            v-model="registData.captchaCode"
                            auto-complete="off"
                            size="large"
                            class="flex-1"
                            :placeholder="$t('login.captchaCode')"
                            @keyup.enter="handleRegistSubmit"
                        />
                        <CaptchaCode
                            ref="captcha"
                            class="captcha-image"
                            @update-captcha-code="getCaptcha"
                        />
                    </div>
                </el-form-item>
                <!--Login-Button-->
                <div class="flex justify-between">
                    <el-button
                        :loading="loading"
                        type="primary"
                        size="large"
                        class="w-1/2"
                        @click.prevent="
                            () => {
                                router.push({ path: '/login', query: {} })
                            }
                        "
                        >{{ $t('login.back') }}
                    </el-button>
                    <el-button
                        :loading="loading"
                        type="primary"
                        size="large"
                        class="w-1/2"
                        @click.prevent="handleRegistSubmit"
                        >{{ $t('login.register') }}
                    </el-button>
                </div>
                <!-- <div class="mt-10 text-sm">
                    <span>{{ $t('login.username') }}: admin</span>
                    <span class="ml-4"> {{ $t('login.password') }}: 123456</span>
                </div> -->
            </el-form>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { type LocationQuery, useRoute } from 'vue-router'
import router from '@/router'
import defaultSettings from '@/config/settings'
import { ThemeEnum } from '@/enums/themeEnum'
import type { RegistData } from '@/api/auth'
import { ElMessage, type FormInstance } from 'element-plus'
import { useSettingsStore, useUserStore } from '@/stores'
import '@/styles/login.scss'
import CaptchaCode from '@/components/Captcha/index.vue'

const userStore = useUserStore()
const settingsStore = useSettingsStore()
const route = useRoute()
const captcha = ref()

const { t } = useI18n()
const isDark = ref(settingsStore.themeMode === ThemeEnum.DARK)

const loading = ref(false)
const isCapslock = ref(false)
const registFormRef = ref<FormInstance>()
let curCaptchaCode = ref()
const registData = ref<RegistData>({
    username: '',
    password: '',
    repassword: '',
    captchaCode: ''
} as RegistData)

const validateCaptchaCode = (rule: any, value: string, callback: any) => {
    value = value.toUpperCase()
    if (value !== curCaptchaCode.value) {
        console.log('value: ' + value)
        console.log('curCaptchaCode: ' + curCaptchaCode.value)
        // callback(new Error(t('login.message.captcha.error')))
        captcha.value.refreshCode()
    } else {
        callback()
        // callback()
    }
}

function handlejump() {
    router.push({ path: '/home', query: {} })
}

const loginRules = computed(() => {
    return {
        username: [
            {
                required: true,
                triggered: 'blur',
                message: t('login.message.username.required')
            }
        ],
        password: [
            {
                required: true,
                triggered: 'blur',
                message: t('login.message.password.required')
            },
            {
                min: 6,
                triggered: 'blur',
                message: t('login.message.password.min')
            }
        ],
        repassword: [
            {
                required: true,
                triggered: 'blur',
                message: t('login.message.password.required')
            },
            {
                min: 6,
                triggered: 'blur',
                message: t('login.message.password.min')
            },
            {
                validator: (rule: any, value: any, callback: any) => {
                    if (value !== registData.value.password) {
                        callback(new Error(t('login.message.password.match')))
                    } else {
                        callback()
                    }
                },
                triggered: 'blur'
            }
        ],
        captchaCode: [
            {
                required: true,
                trigger: 'blur',
                message: t('login.message.captcha.required')
            },
            {
                validator: validateCaptchaCode,
                trigger: 'blur'
            }
        ]
    }
})

function handleRegistSubmit() {
    registFormRef.value?.validate(async (valid: boolean) => {
        if (valid) {
            loading.value = true
            try {
                const res = await userStore.regist(registData.value)
                loading.value = false
                router.push('/login')
            } catch (error) {
                console.log(error)
                loading.value = false
            }
        } else {
            ElMessage({
                type: 'error',
                message: t('login.message.registFailed')
            })
            captcha.value.refreshCode()
        }
    })
}

function getCaptcha(data: string) {
    curCaptchaCode.value = data
}

const toggleTheme = () => {
    const newTheme = settingsStore.themeMode === ThemeEnum.DARK ? ThemeEnum.LIGHT : ThemeEnum.DARK
    settingsStore.setThemeMode(newTheme)
}

function checkCapslock(event: KeyboardEvent) {
    if (event instanceof KeyboardEvent) {
        isCapslock.value = event.getModifierState('CapsLock')
    }
}
onMounted(() => {})
</script>

<style></style>
