import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getWalletSummary } from 'src/services/walletServis'
import { showError } from 'src/utils/toast'

export const useDonatChartStore = defineStore('donatChart', () => {
  const assets = ref([])
  const totalValue = ref(0)
  const isLoading = ref(false)

  // Visual settings (frontend only)
  const assetColorMap = {
    'طلا خام': '#E7C24D',
    'نقره خام': '#8F8F8F',
    'موجودی ریالی': '#64C2A7',
    'شمش': '#E2563D',
    'پلاتین': '#9B59B6'
  }

  const assetIconMap = {
    gold: 'gold',
    silver: 'silver',
    rial: 'dollar',
    ignot: 'shemsh',
    platinum: 'platinum',
    default: 'coin'
  }

  // Real API call
  async function fetchDonatChartData() {
    isLoading.value = true
    try {
      const response = await getWalletSummary()

      const enriched = response.assets.map(asset => ({
        ...asset,
        icon: assetIconMap[asset.slug] || assetIconMap.default,
        color: assetColorMap[asset.name] || '#CCCCCC'
      }))

      assets.value = enriched
      totalValue.value = response.total_value
    } catch (error) {
      console.error('❌ Failed to fetch wallet summary:', error)
      showError('دریافت اطلاعات ناموفق')
    } finally {
      isLoading.value = false
    }
  }

  // Chart.js compatible data
  const chartData = computed(() => ({
    labels: assets.value.map(a => a.name),
    datasets: [
      {
        data: assets.value.map(a => a.data),
        backgroundColor: assets.value.map(a => a.color),
        borderColor: 'rgba(255, 255, 255, 1)',
        borderWidth: 2
      }
    ]
  }))

  return {
    assets,
    totalValue,
    chartData,
    isLoading,
    fetchDonatChartData
  }
})
