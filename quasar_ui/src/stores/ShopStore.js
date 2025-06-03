import { ref } from "vue";
import { defineStore } from "pinia";
import { getShopProducts, getShopProductsById } from "src/services/shopService";


export const useShopStore = defineStore('shop', () => {
  const products = ref([])
  const selectedProduct = ref(null)
  const isLoading = ref(false)

  async function fetchShopProducts(filters){
    isLoading.value = true
    try{
      const response = await getShopProducts(filters)
      products.value = response.products
    }catch(err){
      console.log(err)
    }finally{
      isLoading.value = false
    }
  }
  async function fetchShopProductsById(id){
    isLoading.value = true
    try{
      const response = await getShopProductsById(id)
      selectedProduct.value = response
    }catch(err){
      console.log(err)
    }finally{
      isLoading.value = false
    }
  }

  return{
    products,
    selectedProduct,
    fetchShopProducts,
    fetchShopProductsById
  }
})
