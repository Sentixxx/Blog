import request from '@/utils/request'

const USER_BASE_URL = import.meta.env.VITE_APP_BASE_API + '/user'

class UserAPI {
    /**
     * @returns 用户名称，头像，权限等
     */
    static getInfo() {
        return request<any, UserInfo>({
            url: `${USER_BASE_URL}/info`,
            method: 'get'
        })
    }
}

export default UserAPI

export interface UserInfo {
    /** 用户ID */
    userId?: number
    /** 用户名 */
    username?: string
    /** 昵称 */
    nickname?: string
    /** 头像URL */
    avatar?: string
    /** 用户组 */
    group: string
    /** 权限 */
    perms?: string[]
    /** 邮箱 */
    email?: string
    /** 手机号 */
    mobile?: string
    /** 性别 */
    gender?: string
}
