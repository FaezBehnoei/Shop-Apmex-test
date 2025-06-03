import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getAssetDetail } from 'src/services/walletServis'

export const useAssetDetailStore = defineStore('assetDetail', () => {
  const asset        = ref(null)
  const transactions = ref([])
  const isLoading    = ref(false)

  // اینجا ساختار اولیه‌ی rawChartData رو با همه‌ی کلیدها درنظر می‌گیریم
 const rawChartData = ref({
  '24h':   { data: [], summary: { profit_percent: 0 } },
  '1w':    { data: [], summary: { profit_percent: 0 } },
  '1m':    { data: [], summary: { profit_percent: 0 } },
  '3m':    { data: [], summary: { profit_percent: 0 } },
  '1y':    { data: [], summary: { profit_percent: 0 } }
})


const timestamps = ref([])


  const profitIndicators = computed(() => {
    const d = rawChartData.value
    return [
      { label: '۲۴ ساعت اخیر', value: '24h', profit:  d['24h']?.summary.profit_percent || 0 },
      { label: 'هفته اخیر',    value: '1w',  profit:  d['1w']?.summary.profit_percent  || 0 },
      { label: 'ماه اخیر',     value: '1m',  profit:  d['1m']?.summary.profit_percent  || 0 },
      { label: '۱ سال اخیر',   value: '1y',  profit:  d['1y']?.summary.profit_percent  || 0 },
    ]
  })

  const colorsMap = {
    gold:  '#E7C24D',
    silver:'#8F8F8F',
    rial:  '#64C2A7',
    ignot: '#E2563D',
  }
  const transactionsStatusMap = { 1:"ناموفق",2:"در حال انجام",3:"موفق" }

  async function fetchAssetDetail(slug) {
    isLoading.value = true
    try {
      const [response] = await getAssetDetail(slug)
      response.asset.color = colorsMap[response.asset.slug]
      asset.value = response.asset

      transactions.value = response.transactions.map(tx => ({
        ...tx,
        statusText: transactionsStatusMap[tx.status]
      }))

      // پر کردن rawChartData با چیزی که از API میاد
      rawChartData.value = response.chart_data
      timestamps.value = response.timestamps

    }
    finally { isLoading.value = false }
  }


  return {
    asset,
    transactions,
    isLoading,
    rawChartData,
    timestamps,
    profitIndicators,
    fetchAssetDetail
  }
})
