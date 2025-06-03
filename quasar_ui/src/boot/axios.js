// src/boot/axios.js
import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { useAuthStore } from 'src/stores/auth'

const persianDigits = '۰۱۲۳۴۵۶۷۸۹'
const englishDigits = '0123456789'

function toEnglishNum(str) {
  return typeof str === 'string'
    ? str.replace(/[۰-۹]/g, ch => englishDigits[persianDigits.indexOf(ch)])
    : str
}

function deepConvert(obj) {
  if (typeof obj === 'string') return toEnglishNum(obj)
  if (Array.isArray(obj)) return obj.map(deepConvert)
  if (typeof obj === 'object' && obj !== null) {
    const out = {}
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        out[key] = deepConvert(obj[key])
      }
    }
    return out
  }
  return obj
}

const api = axios.create({
  baseURL: 'https://shop-apmex-test.onrender.com',
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {

    if (!config.skipDigitConvert) {
      if (config.data) config.data = deepConvert(config.data)
      if (config.params) config.params = deepConvert(config.params)
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      if (!authStore.isAuthenticated) {
        authStore.logout()
      }
      return Promise.reject(error)
    }

    if (error.response?.status === 403) {
      console.error('Forbidden request:', error)
    } else if (error.response?.status === 422) {
      console.error('Validation error:', error.response.data)
    } else if (error.response?.status === 500) {
      console.error('Server error:', error)
    }

    return Promise.reject(error)
  }
)

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }
