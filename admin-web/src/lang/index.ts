import type {App} from "vue"
import { createI18n } from 'vue-i18n'
import enLocale from "./package/en"
import zhcnLocale from "./package/zh-cn"
import en from "./package/en"

const messages = {
    "zh-cn": {
        ...zhcnLocale,
    },
    "en": {
        ...enLocale,
    }
}

