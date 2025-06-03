// src/directives/v-num-fa.js
const persianDigits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹']
const englishDigits = ['0','1','2','3','4','5','6','7','8','9']

function toPersianNum(str) {
  return str.replace(/\d/g, d => persianDigits[d])
}
function toEnglishNum(str) {
  return str.replace(/[۰-۹]/g, d => englishDigits[persianDigits.indexOf(d)])
}

export default {
  mounted(el) {
    if (!el.matches('input, textarea')) return

    el.value = toPersianNum(toEnglishNum(el.value))

    el.addEventListener('input', e => {
      const raw = e.target.value
      const cleaned = toEnglishNum(raw)
      const formatted = toPersianNum(cleaned)

      if (raw !== formatted) {
        e.target.value = formatted
        e.target.dispatchEvent(new Event('input', { bubbles: true }))
      }
    })
  }
}
