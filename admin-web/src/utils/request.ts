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
        console.log(error)
        Promise.reject(error)
    }
)

service.interceptors.response.use(
    (response: AxiosResponse) => {
        // 检查配置的响应类型是否为二进制类型（'blob' 或 'arraybuffer'）, 如果是，直接返回响应对象
        if (
            response.config.responseType === 'blob' ||
            response.config.responseType === 'arraybuffer'
        ) {
            return response
        }

        const { code, data, msg } = response.data
        if (code === ResultEnum.SUCCESS) {
            return data
        }

        ElMessage.error(msg || '系统出错')
        return Promise.reject(new Error(msg || 'Error'))
    },
    (error) => {
        console.log('err' + error)
        // 异常处理
        if (error.response.data) {
            const { code, msg } = error.response.data
            if (code === ResultEnum.TOKEN_INVALID) {
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
            } else {
                ElMessage.error(msg || '系统出错')
            }
        }
        return Promise.reject(error)
    }
)

export default service
