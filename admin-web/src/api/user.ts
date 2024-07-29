import request from '@/utils/request'

const USER_BASE_URL = '/user'

class UserAPI {
    /**
     * @returns 用户名称，头像，权限等
     */
    static getInfCur(): Promise<UserInfo> {
        return request<any, UserInfo>({
            url: `${USER_BASE_URL}/info/cur`,
            method: 'get'
        })
    }
    static getInfo(): Promise<UserInfo> {
        return request<any, UserInfo>({
            url: `${USER_BASE_URL}/info`,
            method: 'get'
        })
    }
}

export default UserAPI

export interface UserInfo {
    /** 用户ID */
    user_instance_id: number
    /** 用户名 */
    user_instance_name?: string
    /** 昵称 */
    user_instance_nickname?: string
    /** 头像URL */
    user_instance_avatar?: string
    /** 用户组 */
    user_instance_group_name: string
    /** 权限 */
    perms?: string[]
    /** 邮箱 */
    user_instance_email?: string
    /** 手机号 */
    user_instance_mobile?: string
    /** 性别 */
    user_instance_gender?: string
    user_instance_status?: number
}
