import AuthAPI from '@/api/auth'
import UserAPI from '@/api/user'
import { resetRouter } from '@/router'
import { store } from '@/stores'
import type { LoginData } from '@/api/auth'
import type { UserInfo } from '@/api/user'
import { TOKEN_KEY } from '@/enums/cacheEnum'

export const useUserStore = defineStore('user', () => {
    const user = ref<UserInfo>({
        group: ''
    })

    /**
     * 登录
     * @param {LoginData} data 登录数据
     * @returns {Promise<void>}
     */
    function login(loginData: LoginData): Promise<void> {
        return new Promise<void>((resolve, reject) => {
            AuthAPI.login(loginData)
                .then((data: any) => {
                    const { tokenType, accessToken } = data
                    localStorage.setItem(TOKEN_KEY, tokenType + ' ' + accessToken)
                    resolve()
                })
                .catch((error: any) => {
                    reject(error)
                })
        })
    }

    function getUserInfo(): Promise<void> {
        return new Promise<void>((resolve, reject) => {
            UserAPI.getInfo()
                .then((data: any) => {
                    if (!data) {
                        reject(new Error('Verification failed, please Login again.'))
                        return
                    }
                    Object.assign(user.value, { ...data })
                    resolve(data)
                })
                .catch((error: any) => {
                    reject(error)
                })
        })
    }

    function logout(): Promise<void> {
        return new Promise<void>((resolve, reject) => {
            AuthAPI.logout()
                .then(() => {
                    localStorage.setItem(TOKEN_KEY, '')
                    location.reload()
                    resolve()
                })
                .catch((error: any) => {
                    reject(error)
                })
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
