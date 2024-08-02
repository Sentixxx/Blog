import AuthAPI from '@/api/auth'
import UserAPI from '@/api/user'
import { resetRouter } from '@/router'
import { store } from '@/stores'
import type { LoginData, RegistData } from '@/api/auth'
import type { UserInfo } from '@/api/user'
import { TOKEN_KEY } from '@/enums/cacheEnum'

export const useUserStore = defineStore('user', () => {
    const user = ref<UserInfo>({
        user_instance_group_name: 'user',
        user_instance_name: '访客',
        user_instance_avatar:
            'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        user_instance_id: -1
    })

    /**
     * 登录
     * @param {LoginData} data 登录数据
     * @returns {Promise<void>}
     */
    async function login(loginData: LoginData): Promise<void> {
        try {
            const data = await AuthAPI.login(loginData)
            const { tokenType, accessToken } = data
            localStorage.setItem(TOKEN_KEY, `${tokenType} ${accessToken}`)
            await getUserInfo()
            // console.log('store sucess')
        } catch (error) {
            return Promise.reject(error)
        }
    }
    async function regist(reigstData: RegistData): Promise<void> {
        try {
            const data = await AuthAPI.regist(reigstData)
        } catch (error) {
            return Promise.reject(error)
        }
    }
    async function getUserInfo(): Promise<void> {
        try {
            const data = await UserAPI.getInfoCur()
            if (!data) {
                throw new Error('Verification failed, please Login again.')
            }
            Object.assign(user.value, { ...data })
            if (user.value.user_instance_avatar === null) {
                user.value.user_instance_avatar =
                    'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
            }
        } catch (error) {
            console.error(error)
        }
    }

    function logout(): Promise<void> {
        return new Promise<void>((resolve, reject) => {
            localStorage.setItem(TOKEN_KEY, '')
            location.reload()
            resolve()
        })
    }

    function resetToken(): Promise<void> {
        console.log('resetToken')
        return new Promise<void>((resolve) => {
            localStorage.setItem(TOKEN_KEY, '')
            resetRouter()
            resolve()
        })
    }

    return {
        user,
        login,
        regist,
        getUserInfo,
        logout,
        resetToken
    }
})

export function useUserStoreHook() {
    return useUserStore(store)
}
