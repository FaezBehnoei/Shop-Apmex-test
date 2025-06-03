// validation.js
export const rules = {
  required: (value) => !!value || 'این فیلد الزامی است',
  email: (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return !value || pattern.test(value) || 'ایمیل وارد شده معتبر نیست'
  },
  minLength: (min) => (value) =>
    !value || value.length >= min || `حداقل باید ${min} کاراکتر داشته باشد`,
  maxLength: (max) => (value) =>
    !value || value.length <= max || `حداکثر می‌تواند ${max} کاراکتر داشته باشد`,
  numeric: (value) =>
    !value || /^\d+$/.test(value) || 'فقط عدد وارد کنید',
  match: (field, fieldName) => (value, formValues) =>
    !value || value === formValues[field] || `باید با ${fieldName} یکسان باشد`,
  
}

export const validate = (value, fieldRules = [], formValues = {}) => {
  if (!fieldRules.length) return { valid: true, message: '' }

  for (const rule of fieldRules) {
    const result = typeof rule === 'function' ? rule(value, formValues) : rule

    if (result !== true && typeof result === 'string') {
      return { valid: false, message: result }
    }
  }

  return { valid: true, message: '' }
}
