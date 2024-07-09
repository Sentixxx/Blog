import type {App} from "vue"
import { createI18n } from 'vue-i18n'
import enLocale from "./package/en"
import zhcnLocale from "./package/zh-cn"
import { useAppStoreHook } from "@/stores"

const appStore = useAppStoreHook();

const messages = {
    "zh-cn": {
        ...zhcnLocale,
    },
    "en": {
        ...enLocale,
    }
}

const i18n = createI18n({
    legacy: false,
    locale: appStore.language,
    message: messages,
    globalInjection: true,
});

export function setupI18n(app:App<Element>) {
    app.use(i18n);
}

export default i18n;

