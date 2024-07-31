import request from '@/utils/request'
import { UserInfo } from './user'

const AUTH_BASE_URL = ''

class AuthAPI {
    static login(data: LoginData) {
        return request<any, LoginResult>({
            url: `${AUTH_BASE_URL}/login`,
            method: 'POST',
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            params: {
                user_instance_name: data.username,
                user_instance_password: data.password
            }
        })
    }
}

export default AuthAPI

export interface LoginData {
    username: string
    password: string
    captchaKey: string
    captchaCode: string
}
export interface LoginResult {
    accessToken?: string
    expires?: number
    refreshToken?: string
    tokenType?: string
    user_info?: UserInfo
}

/** 验证码响应 */
export interface CaptchaResult {
    /** 验证码缓存key */
    captchaKey: string
    /** 验证码图片Base64字符串 */
    captchaBase64: string
}
