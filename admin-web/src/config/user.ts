import { App } from 'vue'
import { useUserStore } from '@/stores'

export default async function setupUserInfo(app: App<Element>) {
    const userStore = useUserStore()
    await userStore.getUserInfo()
}
