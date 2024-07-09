import AuthAPI from '@/api/auth';
import UserAPI from '@/api/user';
import { resetRouter } from '@/router';
import { store } from '@/stores';
import type { LoginData } from '@/api/auth';
import type { UserInfo } from '@/api/user';
import { TOKEN_KEY } from '@/enums/cacheEnum';

export const useUserStore = defineStore("user", () => {
    const user = ref<UserInfo>({
        roles: [],
        perms: [],
    });

    /**
     * 登录
     * @param {LoginData} data 登录数据
     * @returns {Promise<void>}
     */
    function login(loginData: LoginData){
        return new Promise<void>((resolve,reject) => {
            AuthAPI.login(loginData)
            .then((data : any) => {
                const { tokenType, accessToken } = data;
                localStorage.setItem(TOKEN_KEY,tokenType + " " + accessToken);
                resolve();
            })
            .catch((error : any) => {
                reject(error);
            });
        });
    }

    function getUserInfo() {
        return new Promise<void>((resolve,reject) => {
            UserAPI.getInfo()
            .then((data : any) => {
                if(!data) {
                    reject(new Error("Verification failed, please Login again."));
                    return;
                }
                if(!data.roles || data.roles.length <= 0) {
                    reject("getInfo: roles must be a non-null array!");
                    return;
                }
                Object.assign(user.value,{...data});
                resolve(data);
            })
            .catch((error : any) => {
                reject(error);
            });
        });
    }

    function logout() {
        return new Promise<void>((resolve,reject) => {
            AuthAPI.logout()
            .then(() => {
                localStorage.setItem(TOKEN_KEY,"");
                location.reload();
                resolve();
            })
            .catch((error : any) => {
                reject(error);
            });
        });
    }

    function resetToken() {
        console.log("resetToken");
        return new Promise<void>((resolve) => {
            localStorage.setItem(TOKEN_KEY,"");
            resetRouter();
            resolve();
        });
    }

    return {
        user,
        login,
        getUserInfo,
        logout,
        resetToken,
    };
});

export function useUserStoreHook() {
    return useUserStore(store);
}

