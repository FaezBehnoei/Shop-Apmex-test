import { api } from 'src/boot/axios'
import { showError, showSuccess } from 'src/utils/toast'

/**
 * Fetch wallet summary (used in Donat Chart)
 */
export async function getWalletSummary() {
  const { data } = await api.get('/wallet/summary')
  return data
}

/**
 * Fetch detailed info of a single asset (with transactions + chart data)
 */
export async function getAssetDetail(slug) {
  const { data } = await api.get(`/wallet/asset-detail/${slug}`)
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

/**
 * Fetch wallet asset
 */
export async function getWalletAssets() {
  const { data } = await api.get('/wallet/assets')
  return data
}

/**
 * Submit a withdrawal request
 */
export async function submitWithdrawRequest(payload) {
  const { data } = await api.post('/wallet/withdraw', payload)
  return data
}

/**
 * get products shop wallet
 */

export async function getProductsShopWallet(filter) {
  const params = {}

  if (filter !== 'all') {
    params.category = filter
  }

  const { data } = await api.get('/wallet/shop-products', { params })
  return data
}

/**
 * get products shop wallet
 */
export async function getProductByIdWallet(id) {
  const { data } =  await api.get(`/wallet/shop-products/${id}`)
  return data
}

/**
 * get Addresses and timeStamps
 */
export async function getAddressAndTimeStampWallet(method) {
  const params = {}
  params.method = method
  const { data } = await api.get('/wallet/addresses-with-timestamps', { params })
  return data
}

/**
 * post selected Address and time in delivery confirm
 */
export async function confirmPickedUpProductWallet(pickUpData){
  const { data } = await api.post('/wallet/confirm-pickup', pickUpData)
  return data
}


/**
 * Submit a wallet deposit request
 */
export async function depositToWallet(payload) {
  const { data } = await api.post('/wallet/deposit', payload)
  showSuccess('درخواست با موفقیت ثبت شد')
  return data
}

/**
 * get popular numbers deposit request
 */
export async function getQuickNumbersWallet() {
  const { data } = await api.get('/wallet/quick-amounts')
  return data
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
