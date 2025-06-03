import { api } from 'src/boot/axios'
import { showError } from 'src/utils/toast'

/**
 * Login
 */
export async function loginWithPassword({ identifier, password }) {
  const { data } = await api.post('/auth/login', { identifier, password })
  return data
}

/**
 * Otp Request
 */
export async function requestOtp({phoneNumber}) {
  const { data } = await api.post('/auth/request-otp', {
    identifier: phoneNumber
  })
  return data
}

/**
 * Otp Request
 */
export async function requestOtpFogrgetPassword({phoneNumber}) {
  const { data } = await api.post('/auth/forgot-password', {
    phone_number: phoneNumber
  })
  return data
}

/**
 * OTP Verification
 */
export async function verifyOtp({ otpCode, otpToken }) {
  const { data } = await api.post('/auth/verify-otp', {
    otp_code: otpCode,
    otp_token: otpToken
  })
  return data
}

/**
 * OTP reset password Verification
 */
export async function verifyOtpResetPassword({ otpCode, otpToken }) {
  const { data } = await api.post('/auth/verify-reset-otp', {
    otp_code: otpCode,
    otp_token: otpToken
  })
  return data
}

/**
 * New Password
 */
export async function resetPassword({  newPassword , otpToken}) {
  const { data } = await api.post('/auth/reset-password', {
    new_password: newPassword,
    otp_token:otpToken
  })
  return data
}

/**
 * Sign-Up
 */
export async function verifyNationalIdAndPhone({ nationalId, phoneNumber }) {
  const { data } = await api.post('/auth/initiate-registration', {
    national_id: nationalId,
    phone_number: phoneNumber,
    accept_terms: true
  })
  return data
}

/**
 * Validate Invite Code
 */
export async function validateInviteCode({ inviteCode }) {
  const { data } = await api.post('/auth/validate-invite', {
    invite_code: inviteCode
  })
  return data
}

/**
 * Invite Code and Set Password
 */
export async function completeSignup({ password, inviteCode , phoneNumber}) {
  const { data } = await api.post('/auth/register', {
    password,
    invite_code: inviteCode,
    phone_number:phoneNumber
  })
  return data
}

/**
 * Logout
 */
export async function logoutUser() {
  await api.post('/auth/logout')
}

// Error handling should now be used only in components:
export const errorMessageMap = {
  'Invalid credentials': 'نام کاربری یا رمز عبور اشتباه است.',
  'OTP expired': 'کد تایید منقضی شده است.',
  'OTP incorrect': 'کد تایید اشتباه است.',
  'National ID and phone number do not match': 'کد ملی و شماره همراه مطابقت ندارند.',
  'Invite code is invalid': 'کد دعوت نامعتبر است.',
  'User not found': 'کاربری با این مشخصات یافت نشد.',
  'Password too weak': 'رمز عبور باید حداقل ۸ کاراکتر و شامل عدد و حرف باشد.',
  // پیام‌های بیشتر را اینجا اضافه کن
}

/**
 * Error Handling
 */

export function handleError(error, fallbackMessage = 'خطایی رخ داده است') {
  let message = fallbackMessage

  const status = error?.response?.status
  const rawMessage =
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    ''

  if (rawMessage && errorMessageMap[rawMessage]) {
    message = errorMessageMap[rawMessage]
  } else {
    switch (status) {
      case 400:
        message = 'درخواست نامعتبر بود.'
        break
      case 401:
        message = 'لطفاً وارد حساب کاربری شوید.'
        break
      case 403:
        message = 'شما اجازه این عملیات را ندارید.'
        break
      case 404:
        message = 'موردی یافت نشد.'
        break
      case 422:
        message = 'اطلاعات وارد شده صحیح نیست.'
        break
      case 500:
        message = 'خطا از سمت سرور رخ داده است.'
        break
    }
  }

  showError(
    message)

  if (process.env.DEV) {
    console.error('❌ Error:', error)
  }
}
