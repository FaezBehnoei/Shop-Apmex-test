// src/boot/auto-digit-convert.js
import { boot } from 'quasar/wrappers'
import VNumFa from 'src/directives/v-num-fa'

const persianDigits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹']
const englishDigits = ['0','1','2','3','4','5','6','7','8','9']

const toEnglishNum = str =>
  typeof str === 'string'
    ? str.replace(/[۰-۹]/g, ch => englishDigits[persianDigits.indexOf(ch)])
    : str

const deepConvert = obj => {
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

export default boot(({ app }) => {
  // ۱) دایرکتیو سراسری: v-num-fa
  app.directive('num-fa', VNumFa)

  // ۲) متدهای تبدیل در دسترس Vue
  app.config.globalProperties.$toEnglishNum = toEnglishNum

  // ۳) axios interceptor
  const axios = app.config.globalProperties.$axios
  if (axios) {
    axios.interceptors.request.use(cfg => {
      if (cfg.headers?.['skip-digit-convert'] || cfg.skipDigitConvert) {
        delete cfg.headers['skip-digit-convert']
        return cfg
      }

      if (cfg.data) cfg.data = deepConvert(cfg.data)
      if (cfg.params) cfg.params = deepConvert(cfg.params)
      return cfg
    })
  }
})
