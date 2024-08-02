import { useUserStore } from '@/stores'

const userStore = useUserStore()

export function isAdmin() {
    if (userStore.user.user_instance_group_name.includes('admin')) {
        // console.log(userStore.user.user_instance_group_name.includes('admin'))
        return true
    }
    return false
}
