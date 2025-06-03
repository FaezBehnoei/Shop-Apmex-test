import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { getFilteredWalletTransactions } from 'src/services/walletServis'

export const useTransactionsStore = defineStore('transactions', () => {
  // --- state ---
  const transactions = ref([])
  const loading = ref(false)
  const error = ref(null)

  const filters = ref({
    dateFrom: '',
    dateTo: '',
    status: 'همه',     // 1=ناموفق | 2=درحال انجام | 3=موفق
    type: 'همه',       // مثل: واریز، برداشت، ...
    amountFrom: '',
    amountTo: '',
    search: '',
    category: 'all'    // مثل: طلا، نقره، شمش
  })

  // --- computed: mapping color and text ---
  const mappedTransactions = computed(() => {
    const statusColorMap = {
      3: 'text-green',         // موفق
      1: 'text-red',         // ناموفق
      2: 'text-orange-primary'    // درحال انجام
    }

    const statusTextMap = {
      3: 'موفق',
      1: 'ناموفق',
      2: 'درحال انجام'
    }

    return transactions.value.map(tx => {
      // رنگ‌دهی پویا برای نوع تراکنش
      let typeColor = 'text-grey'
      const type = tx.type || ''

      if (type.includes('واریز')) {
        typeColor = 'text-green'
      } else if (type.includes('برداشت')) {
        typeColor = 'text-red'
      } else if (type.includes('تبدیل')) {
        typeColor = 'text-blue-custom'
      } else if (type.includes('خرید')) {
        typeColor = 'text-green'
      } else if (type.includes('فروش')) {
        typeColor = 'text-red'
      }

      return {
        ...tx,
        statusText: statusTextMap[tx.status] || 'نامشخص',
        statusColor: statusColorMap[tx.status] || 'text-grey',
        typeColor
      }
    })
  })

  // --- computed: group by date ---
  const groupedTransactions = computed(() => {
    return mappedTransactions.value.reduce((groups, tx) => {
      (groups[tx.date] = groups[tx.date] || []).push(tx)
      return groups
    }, {})
  })

  // --- action: apply filters and fetch data ---
  const applyFilters = async (newFilters = {}) => {
    filters.value = { ...filters.value, ...newFilters }
    await fetchTransactions()
  }

  // --- action: fetch data from API ---
  const fetchTransactions = async () => {
    loading.value = true
    error.value = null

    try {
      const data = await getFilteredWalletTransactions(filters.value)
      console.log(data)
      transactions.value = data.transactions || []
    } catch (err) {
      error.value = err
    } finally {
      loading.value = false
    }
  }

  return {
    // state
    transactions,
    loading,
    error,
    filters,

    // actions
    applyFilters,
    fetchTransactions,

    // computed
    mappedTransactions,
    groupedTransactions
  }
})
