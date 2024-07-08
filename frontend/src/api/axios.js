import axios from 'axios'
import { ElMessage } from 'element-plus'

export const CreateAxiosInstance = (config) => {
  const service = axios.create({
    timeout: 5000,
    baseURL: '/api',
    ...config
  })

  service.interceptors.request.use(
    (config) => {
      //DO sth before request is sent
      return config
    },
    (error) => {
      console.log(error)
      Promise.reject(error)
    })

  service.interceptors.response.use(
    (response) => {
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
    })
  return service
}

const request = CreateAxiosInstance({})
export default request