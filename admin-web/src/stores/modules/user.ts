import AuthAPI from '@/api/auth'
import UserAPI from '@/api/user'
import { resetRouter } from '@/router'
import { store } from '@/stores'
import type { LoginData } from '@/api/auth'
import type { UserInfo } from '@/api/user'
import { TOKEN_KEY } from '@/enums/cacheEnum'

export const useUserStore = defineStore('user', () => {
    const user = ref<UserInfo>({
        user_instance_group_name: 'user',
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
    async function getUserInfo(): Promise<void> {
        try {
            const data = await UserAPI.getInfoCur()
            if (!data) {
                throw new Error('Verification failed, please Login again.')
            }
            Object.assign(user.value, { ...data })
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
        getUserInfo,
        logout,
        resetToken
    }
})

export function useUserStoreHook() {
    return useUserStore(store)
}
