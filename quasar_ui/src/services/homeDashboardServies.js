import { api } from 'src/boot/axios'
import { showError } from 'src/utils/toast'

/**
 * Fetch metals for dashboard (gold, silver, etc.)
 */
export async function getDashboardMetals() {
  const { data } = await api.get('/dashboard/metals')
  return data
}

/**
 * Fetch user orders for dashboard
 */
export async function getDashboardOrders() {
  const { data } = await api.get('/dashboard/orders')
  return data
}

/**
 * Fetch chart data for dashboard
 */
export async function getDashboardChart() {
  const { data } = await api.get('/dashboard/chart')
  return data
}



/**
 * Fetch product categories shown on dashboard
 */
export async function getDashboardCategories() {
  const { data } = await api.get('/dashboard/categories')
  return data
}

/**
 * Fetch best-selling products for dashboard
 */
export async function getDashboardBestSellers() {
  const { data } = await api.get('/dashboard/best-sellers')
  return data
}
/**
 * Fetch best-selling news for dashboard
 */
export async function getDashboardNews() {
  const { data } = await api.get('/dashboard/news')
  return data
}


/**
 * Error handling for dashboard API
 */
export function handleDashboardError(error, fallbackMessage = 'خطایی در دریافت اطلاعات داشبورد رخ داد') {
  let message = fallbackMessage
  const status = error?.response?.status
  const rawMessage = error?.response?.data?.detail || error?.response?.data?.message || ''

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
      message = 'اطلاعات یافت نشد.'
      break
    case 500:
      message = 'خطا از سمت سرور رخ داده است.'
      break
  }

  if (rawMessage && errorMessageMap[rawMessage]) {
    message = errorMessageMap[rawMessage]
  }

  showError(
    message)

  if (process.env.DEV) {
    console.error('❌ Dashboard Error:', error)
  }
}

export const errorMessageMap = {
  'Data fetch error': 'خطا در دریافت اطلاعات.',
  'No data available': 'داده‌ای برای نمایش وجود ندارد.'
  // Add more dashboard-specific error messages if needed
}
