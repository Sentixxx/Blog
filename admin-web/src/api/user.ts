import request from '@/utils/request'

const USER_BASE_URL = '/api/users'

class UserAPI {
    /**
     * @returns 用户名称，头像，角色，权限等
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
    /** 角色 */
    roles: string[]
    /** 权限 */
    perms: string[]
}

export interface UserForm {
    /** 用户头像 */
    avatar?: string
    /** 邮箱 */
    email?: string
    /** 性别 */
    gender?: number
    /** 用户ID */
    id?: number
    /** 手机号 */
    mobile?: string
    /** 昵称 */
    nickname?: string
    /** 角色ID集合 */
    roleIds?: number[]
    /** 用户状态(1:正常;0:禁用) */
    status?: number
    /** 用户名 */
    username?: string
}
