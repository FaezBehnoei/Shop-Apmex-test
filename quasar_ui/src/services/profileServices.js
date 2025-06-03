
import { api } from 'src/boot/axios'
import { showError, showToast } from 'src/utils/toast'

/**
 * Fetch current user's profile data
 */
export async function getProfile() {
  try {
    const { data } = await api.get('/profile')
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showError('بارگذاری اطلاعات پروفایل با مشکل مواجه شد.')
    throw error
  }
}
/**
 * Fetch current user's profile data EDIT
 */
export async function getProfileEdit() {
  try {
    const { data } = await api.get('/profile/edit')
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showError('بارگذاری اطلاعات پروفایل با مشکل مواجه شد.')
    throw error
  }
}
/**
 * PUT current user's profile data
 */
export async function submitProfileEdit(profile) {
  try {
    const { data } = await api.put('/profile/edit',profile)
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showError('بارگذاری اطلاعات پروفایل با مشکل مواجه شد.')
    throw error
  }
}

/**
 * Update current user's profile
 * @param {Object} payload  — داده‌های قابل ویرایش پروفایل، مثلاً { fullName, nationalCode, ... }
 */
export async function updateProfile(payload) {
  try {
    const { data } = await api.put('/profile', payload)
    showToast({
      message: 'پروفایل با موفقیت به‌روزرسانی شد.',
      type: 'positive',
      icon: 'check',
      classes: 'my-toast-success'
    })
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.updateProfile error:', error)
    showToast({
      message: 'به‌روزرسانی پروفایل با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}

/**
 * Fetch current Notifications
 */
export async function getProfileNotifications() {
  try {
    const { data } = await api.get('/notifications')
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showToast({
      message: 'بارگذاری اطلاعات با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}
/**
 * Fetch current Notifications Marked
 */
export async function getProfileMarkNotificationsRead(ids) {
  try {
    const { data } = await api.post('/notifications/read', { ids })
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showToast({
      message: 'بارگذاری اطلاعات با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}

/**
 * Fetch current Notifications Marked
 */
export async function getProfileTransactions(filters = {}) {
  try {
    const { data } = await api.get('/profile/transactions', {
      params: {
        search: filters.search || '',
        category: filters.category !== 'all' ? filters.category : undefined
      }
    })
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showToast({
      message: 'بارگذاری اطلاعات با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}

/**
 * Fetch current Notifications Marked
 */
export async function getProfileSHebaBankCards() {
  try {
    const { data } = await api.get('/profile/sheba-cards')
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showToast({
      message: 'بارگذاری اطلاعات با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}
/**
 * Fetch current Notifications Marked
 */
export async function postProfileSHebaBankCard(bank_number) {
  try {
    const { data } = await api.post('/profile/add-sheba', {iban : bank_number})
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showToast({
      message: 'بارگذاری اطلاعات با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}
/**
 * Fetch current Notifications Marked
 */
export async function getProfileInviteCode() {
  try {
    const { data } = await api.get('/profile/invite')
    return data
  }
  catch (error) {
    console.error('❌ ProfileService.getProfile error:', error)
    showToast({
      message: 'بارگذاری اطلاعات با مشکل مواجه شد.',
      type: 'negative',
      icon: 'error',
      classes: 'my-toast-error'
    })
    throw error
  }
}
