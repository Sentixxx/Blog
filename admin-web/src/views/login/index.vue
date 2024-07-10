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
        <!--Login-Form-->
        <el-card class="login-card">
            <div class="text-center relative">
                <h2>{{ defaultSettings.title }}</h2>
                <el-tag class="ml-2 absolute-rt">{{ defaultSettings.version }} </el-tag>
            </div>
            <el-form ref="loginFormRef" :model="loginData" :rules="loginRules" class="login-form">
                <!--Username-->
                <el-form-item prop="username">
                    <div class="input-wrapper">
                        <i-ep-user class="mx-2" /><el-input
                            ref="username"
                            v-model="loginData.username"
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
                                v-model="loginData.password"
                                :placeholder="$t('login.password')"
                                type="password"
                                name="password"
                                @keyup="checkCapslock"
                                @keyup.enter="handleLoginSubmit"
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
                            v-model="loginData.captchaCode"
                            auto-complete="off"
                            size="large"
                            class="flex-1"
                            :placeholder="$t('login.captchaCode')"
                            @keyup.enter="handleLoginSubmit"
                        />
                        <CaptchaCode
                            ref="captcha"
                            class="captcha-image"
                            @update-captcha-code="getCaptcha"
                        />
                    </div>
                </el-form-item>
                <!--Login-Button-->
                <el-button
                    :loading="loading"
                    type="primary"
                    size="large"
                    class="w-full"
                    @click.prevent="handleLoginSubmit"
                    >{{ $t('login.login') }}
                </el-button>
                <div class="mt-10 text-sm">
                    <span>{{ $t('login.username') }}: admin</span>
                    <span class="ml-4"> {{ $t('login.password') }}: 123456</span>
                </div>
            </el-form>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { type LocationQuery, useRoute } from 'vue-router'
import router from '@/router'
import defaultSettings from '@/config/settings'
import { ThemeEnum } from '@/enums/themeEnum'
import type { LoginData } from '@/api/auth'
import { ElMessage, type FormInstance } from 'element-plus'
import { useSettingsStore, useUserStore } from '@/stores'
import '@/styles/login.scss'
import CaptchaCode from '@/components/Captcha/index.vue'

const userStore = useUserStore()
const settingsStore = useSettingsStore()
const route = useRoute()

const { height } = useWindowSize()
const captcha = ref()

const { t } = useI18n()
const isDark = ref(settingsStore.themeMode === ThemeEnum.DARK)

const loading = ref(false)
const isCapslock = ref(false)
const loginFormRef = ref<FormInstance>()
let curCaptchaCode = ref()
const loginData = ref<LoginData>({
    username: 'admin',
    password: '123456'
} as LoginData)

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

const loginRules = computed(() => {
    return {
        username: [
            {
                required: true,
                triggered: 'blur',
                message: t('login.messgae.username.required')
            }
        ],
        password: [
            {
                required: true,
                triggered: 'blur',
                message: t('login.messgae.password.required')
            },
            {
                min: 6,
                triggered: 'blur',
                message: t('login.messgae.password.min')
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

function getCaptcha(data: string) {
    curCaptchaCode.value = data
}

function handleLoginSubmit() {
    loginFormRef.value?.validate((valid: boolean) => {
        if (import.meta.env.VITE_APP_BASE_API === '/dev-api') {
            if (valid) {
                console.log('valid')
            }
            console.log()
            router.push({ path: '/dashboard', query: {} })
        } else {
            if (valid) {
                loading.value = true
                userStore
                    .login(loginData.value)
                    .then(() => {
                        const { path, queryParmas } = parseRedirect()
                        router.push({ path, query: queryParmas })
                    })
                    .catch(() => {
                        captcha.value.refreshCode()
                    })
                    .finally(() => {
                        loading.value = false
                    })
            } else {
                ElMessage({
                    type: 'error',
                    message: t('login.messgae.loginFailed')
                })
            }
        }
    })
}

function parseRedirect(): {
    path: string
    queryParmas: Record<string, string>
} {
    const query: LocationQuery = route.query
    const redirect = (query.redirect as string) ?? '/'
    const url = new URL(redirect, window.location.origin)
    const path = url.pathname
    const queryParmas: Record<string, string> = {}

    url.searchParams.forEach((value, key) => {
        queryParmas[key] = value
    })

    return { path, queryParmas }
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
