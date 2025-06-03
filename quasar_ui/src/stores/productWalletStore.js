import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProductsShopWallet, getProductByIdWallet } from 'src/services/walletServis'

export const useProductStore = defineStore('product', () => {
  const items = ref([])
  const isLoading = ref(false)
  const ignotAmount = ref(0)
  const selectedProduct = ref(null)

  async function fetchProducts(filter = 'all') {
    try {
      isLoading.value = true
      const response = await getProductsShopWallet(filter)
      items.value = response.shopProducts.products || []
      console.log(items.value)
      ignotAmount.value = response.shopProducts.ignotAmount || 0
    } catch (err) {
      console.error('❌ خطا در دریافت محصولات:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchProductByIdWallet(id) {
    try {
      isLoading.value = true
      const response = await getProductByIdWallet(id)
      selectedProduct.value = response.shopProducts || null
    } catch (err) {
      console.error('❌ خطا در دریافت محصول:', err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    items,
    isLoading,
    ignotAmount,
    selectedProduct,
    fetchProducts,
    fetchProductByIdWallet
  }
})
