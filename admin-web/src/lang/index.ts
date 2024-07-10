import type { App } from 'vue'
import { createI18n } from 'vue-i18n'
import { useAppStoreHook } from '@/stores/modules/app'
import enLocale from '@/lang/package/en'
import zhCnLocale from '@/lang/package/zh-cn'

const appStore = useAppStoreHook()

const messages = {
    'zh-cn': {
        ...zhCnLocale
    },
    en: {
        ...enLocale
    }
}

const i18n = createI18n({
    legacy: false,
    locale: appStore.language,
    messages: messages,
    globalInjection: true
})

export function setupI18n(app: App<Element>) {
    app.use(i18n)
}

export default i18n
