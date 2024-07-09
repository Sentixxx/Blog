import request from '@/utils/request';

const AUTH_BASE_URL = '/api/auth';

class AuthAPI {
    static login(data: LoginData) {
        const formData = new FormData();
        formData.append("username",data.username);
        formData.append("password",data.password);
    
        return request<any,LoginResult>({
            url: `${AUTH_BASE_URL}/login`,
            method: 'POST',
            data: formData,
            headers: {
                "Content-Type": "multipart/form-data"
            },
        });

    }

    static logout() {
        return request({
            url: `${AUTH_BASE_URL}/logout`,
            method: 'delete',
        })
    }
}

export default AuthAPI;

export interface LoginData {
    username: string;
    password: string;
}
export interface LoginResult {
    acessToken?: string;
    expires?: number;
    refreshToken?: string;
    tokenType?: string;
}