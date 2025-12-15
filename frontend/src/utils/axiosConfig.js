import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true
});

export default api;

export const setupAxiosInterceptors = () => {
  api.interceptors.request.use(
    config => {
      const token = localStorage.getItem("accessToken")
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    error => Promise.reject(error)
  )
}

export const initializeAuth = () => {
  const token = localStorage.getItem("accessToken")
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`
  }
}
