import request from '@/utils/request'

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

    static logout() {
        return request({
            url: `${AUTH_BASE_URL}/logout`,
            method: 'delete'
        })
    }

    /** 获取验证码 接口*/
    static getCaptcha() {
        return request<any, CaptchaResult>({
            url: `${AUTH_BASE_URL}/captcha`,
            method: 'get'
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
}

/** 验证码响应 */
export interface CaptchaResult {
    /** 验证码缓存key */
    captchaKey: string
    /** 验证码图片Base64字符串 */
    captchaBase64: string
}
