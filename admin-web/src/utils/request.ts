import axios from 'axios';
import type {InternalAxiosRequestConfig, AxiosResponse} from 'axios';
import { ElMessage } from 'element-plus';


const service = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json;charset=UTF-8'
    }
});

service.interceptors.request.use(
    (config : InternalAxiosRequestConfig) => {
        // do something before request is sent
        return config;
    },
    (error) => {
        console.log(error);
        Promise.reject(error);  
    }
);


service.interceptors.response.use(
    (response : AxiosResponse) => {
        return Promise.resolve(response)
    },
    (error) => {
        console.log('err' + error)
        ElMessage({
        message: error.message,
        type: 'error',
        duration: 5 * 1000
        })
        return Promise.reject(error)
    });

    
export default service;