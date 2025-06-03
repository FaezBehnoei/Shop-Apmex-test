import { api } from 'src/boot/axios'
import { showError } from 'src/utils/toast'

/**
 * Fetch shop products
 */
export async function getShopProducts(filters = {}) {
  const { data } = await api.get('/shop/products', {params : filters})
  return data
}

/**
 * Fetch shop products by id
 */
export async function getShopProductsById(id) {
  const { data } = await api.get(`/shop/product-details/${id}`)
  return data
}

/**
 * Fetch wallet transactions with filters (date, status, type, amount, etc.)
 */
export async function getFilteredWalletTransactions(filters = {}) {
  try {
    const { data } = await api.get('/wallet/transactions', {
      params: {
        date_from: filters.dateFrom || undefined,
        date_to: filters.dateTo || undefined,
        status: filters.status !== 'همه' ? filters.status : undefined,
        type: filters.type !== 'همه' ? filters.type : undefined,
        amount_from: filters.amountFrom || undefined,
        amount_to: filters.amountTo || undefined,
        search: filters.search || undefined,
        category: filters.category !== 'all' ? filters.category : undefined
      }
    })
    return data
  } catch (error) {
    handleWalletError(error, 'بارگذاری تراکنش‌ها با مشکل مواجه شد.')
    throw error
  }
}




// Error handling (optional, or shared from auth)
export function handleWalletError(error, fallbackMessage = 'خطایی در کیف پول رخ داده است') {
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
        message = 'اطلاعاتی برای کیف پول یافت نشد.'
        break
      case 422:
        message = 'اطلاعات وارد شده صحیح نیست.'
        break
      case 500:
        message = 'خطا از سمت سرور کیف پول رخ داده است.'
        break
    }
  }

  showError(message)

  if (process.env.DEV) {
    console.error('❌ Wallet Error:', error)
  }
}

// Optional: if using shared errorMessageMap across services
export const errorMessageMap = {
  'Insufficient balance': 'موجودی کافی نیست.',
  'Asset not found': 'دارایی مورد نظر یافت نشد.',
  // Add more wallet-specific messages if needed
}
