import { TOKEN_KEY } from '@/enums/cacheEnum'
import axios from 'axios'
import type { InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage, ElNotification } from 'element-plus'
import { useUserStoreHook } from '@/stores'
import { ResultEnum } from '@/enums/resultEnum'
const service = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json;charset=UTF-8'
    }
})

service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const accessToken = localStorage.getItem(TOKEN_KEY)
        if (accessToken) {
            config.headers.Authorization = accessToken
        }
        return config
    },
    (error) => {
        // console.log('request error')
        console.log(error)
        Promise.reject(error)
    }
)

service.interceptors.response.use(
    (response: AxiosResponse) => {
        const { status, results, msg } = response.data
        // console.log(results)
        if (status === ResultEnum.SUCCESS) {
            ElMessage.success(msg || '操作成功')
            return results
        } else if (status === ResultEnum.TOKEN_INVALID) {
            ElNotification({
                title: '提示',
                message: '您的会话已过期，请重新登录',
                type: 'info'
            })
            useUserStoreHook()
                .resetToken()
                .then(() => {
                    location.reload()
                })
        }

        ElMessage.error(msg || '系统出错')
        return Promise.reject(new Error(msg || 'Error'))
    },
    (error) => {
        // console.log('err' + error)
        // 异常处理
        if (error.response.data) {
            const { msg } = error.response.data
            const { status } = error.response
            // console.log(error.response.status)
            // console.log(status)
            if (status === ResultEnum.TOKEN_INVALID) {
                ElNotification({
                    title: '提示',
                    message: '您的会话已过期，请重新登录',
                    type: 'info'
                })
            } else {
                ElMessage.error(msg || '系统出错')
            }
        }
        return Promise.reject(error)
    }
)

export default service
