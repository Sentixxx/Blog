import axios from 'axios'

export const CreateAxiosInstance = (config) => {
  const instance = axios.create({
    timeout: 3000,
    baseURL: '/api',
    ...config
  })

  instance.interceptors.request.use(
    (config) => config,
    (error) => Promise.reject(error)
  )

  instance.interceptors.response.use(
    (response) => {
      // if (typeof response.data.code != 'number')
      //   return Promise.reject(new APIError({ code: -98, msg: '未知错误，请求损坏' }))
      // if (response.data.code != 200) return Promise.reject(new APIError(response.data))
      return Promise.resolve(response)
    },
    (error) => Promise.reject(error)
  )

  return instance
}

const request = CreateAxiosInstance({})
export default request