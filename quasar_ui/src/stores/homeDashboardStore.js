import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getDashboardMetals,
  getDashboardOrders,
  getDashboardChart,
  getDashboardCategories,
  getDashboardBestSellers,
  handleDashboardError,
  getDashboardNews
} from 'src/services/homeDashboardServies'

export const useHomeStore = defineStore('home', () => {
  const metals = ref([])
  const orders = ref([])
  const chart = ref(null)
  const categories = ref([])
  const bestSellers = ref([])
  const news = ref([])
  const loading = ref(false)

  async function fetchAllDashboardData() {
    loading.value = true
    try {
      const [m, o, c, cat, bs, n] = await Promise.all([
        getDashboardMetals(),
        getDashboardOrders(),
        getDashboardChart(),
        getDashboardCategories(),
        getDashboardBestSellers(),
        getDashboardNews()
      ])

      metals.value = m.content
      orders.value = o.content
      chart.value = c.content
      categories.value = cat.content
      bestSellers.value = bs.content
      news.value = n.content
    } catch (error) {
      handleDashboardError(error)
    } finally {
      loading.value = false
    }
  }

  return {
    metals,
    orders,
    chart,
    categories,
    bestSellers,
    loading,
    news,
    fetchAllDashboardData
  }
})
