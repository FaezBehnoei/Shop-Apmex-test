<template>
  <q-page class="store-page-container">

    <!-- search bar  -->
     <div class="flex items-center justify-between q-mb-md">
      <div class="parent-div">
        <div class="q-ml-md">
          <input v-model="searchQuery" type="text" class="custom-searchQuery full-width" placeholder="جستجو"/>
        </div>
        <SvgIcon name="search" state="black" size="24" class="search-icon"/>
      </div>
      <button @click="openFilterDialog = true" class="bg-white-light-active custom-btn-filter flex flex-center">
        <SvgIcon name="filter" state="black" size="24" />
      </button>
     </div>
    <!-- Header filters -->
    <div>
        <nav class="filter-bar">
          <button
            v-for="f in filters"
            :key="f.value"
            :class="['filter-btn typography-caption-md-regular flex flex-center text-grey-normal', { active: selectedFilter === f.value },{ isAllValue : f.value === 'all'}]"
            @click="selectedFilter = f.value"
          >
            <SvgIcon
              v-if="f.value === 'all'"
              name="search-bar"
              state="black"
              size="24"
              class="q-ml-xs"
            />
            {{ f.label }}
          </button>
        </nav>
       </div>

    <!-- Product Cards Grid -->
    <div class="product-grid">
      <MobileCards
        v-for="product in products"
        :key="product.id"
        :image="[product.image]"
        :title="product.title"
        :ayar="product.ayar"
        :price="product.price"
        :discount="product.discount"
        :discountPrice="product.discountPrice"
        :bestSelling="product.bestSelling"
        class="cursor-pointer"
        @click="goToDetails(product.id)"
        :purchase-shop="true"
      />
    </div>
    <FilterDialogShop v-model:modal-value="openFilterDialog" />
  </q-page>
</template>

<script setup>
import { ref, onMounted, watch} from 'vue';
import MobileCards from 'src/components/MobileCards.vue';
import { useRouter } from 'vue-router';
import SvgIcon from 'src/components/SvgIcon.vue';
import { useShopStore } from 'src/stores/ShopStore';
import FilterDialogShop from 'src/components/Shop/FilterDialogShop.vue';

const router = useRouter();
const selectedFilter = ref('');
const searchQuery = ref('')
const shopStore = useShopStore()
const openFilterDialog = ref(false)

const filters = [
  { label: 'مرتب سازی', value: 'all' },
  { label: 'پرفروش‌ترین‌ها', value: 'most-popular' },
  { label: 'ارزان‌ترین‌ها', value: 'cheapest' },
  { label: 'عیار کمتر', value: 'lower-karat' },
];

const products = ref([]);



function goToDetails(id) {
  router.push({ name: 'product-shop-details', params: { id } });
}
watch([selectedFilter, searchQuery], async ([cat, search]) => {
  await shopStore.fetchShopProducts({
    // اگر فیلتر «همه» (all) انتخاب شد، category را ارسال نکن
    filter: cat && cat !== 'all' ? cat : undefined,
    // اگر جستجو نال یا خالی است، search را ارسال نکن
    search: search?.trim() ? search.trim() : undefined
  })
  products.value = shopStore.products
})


onMounted(async() => {
await shopStore.fetchShopProducts({
    filter: undefined,
    search: undefined
  })
  products.value = shopStore.products
  console.log(products.value)
})
</script>

<style scoped>
.store-page-container {
  padding: 16px;
  padding-bottom: 100px;
}

.filter-bar {
  display: flex;
  overflow-x: auto;
  gap: 1rem; /* 16px */
  scrollbar-width: none;
  margin-bottom: 1.5rem; /* 24px */
}

.filter-btn {
  flex: 0 0 auto;
  border: none;
  cursor: pointer;
  background-color: transparent;
}

.filter-btn.active {
  color: var(--orange-primary);
  font-weight: 500;
  font-size: 0.75rem;   /* 12px */
  line-height: 1.125rem; /* 18px */
  letter-spacing: 0%;
}
.filter-btn.isAllValue{
  font-weight: 700;
  font-size: 14px;
  line-height: 22px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.parent-div {
  position: relative;
  flex: 1;
  max-width: 100%;
}

.custom-searchQuery {
  height: 2.0625rem;         /* 33px */
  padding: 0 2rem 0 0;     /* 0 40px 0 0 */
  border: none;
  border-radius: 0.5rem;     /* 8px */
  background-color: #F0F0F0;
  font-size: 0.875rem;       /* 14px */
  color: #333;
  outline: none;
  box-sizing: border-box;
}

.search-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: 0.5rem; /* 12px */
}

.custom-btn-filter {
  padding: 0.3rem;
  background-color: var(--white-light-active);
  border-radius: 0.256rem; /* 8px */
  border: none;
  cursor: pointer;
}
</style>
