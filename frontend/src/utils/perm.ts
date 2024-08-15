import { useUserStore, useUserStoreHook } from '@/stores'

const userStore = useUserStore()

export function isAdmin() {
    console.log(userStore.user.user_instance_group_name)
    if (userStore.user.user_instance_group_name.includes('admin')) {
        // console.log(userStore.user.user_instance_group_name)
        return true
    }
    return false
}
