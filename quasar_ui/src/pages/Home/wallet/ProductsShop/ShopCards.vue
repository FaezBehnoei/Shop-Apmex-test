<template>
  <q-page class="main-container-shop ">
    <div>
      <!-- header  -->
       <div>
        <nav class="filter-bar">
          <button
            v-for="f in filters"
            :key="f.value"
            :class="['filter-btn typography-caption-lg-regular flex flex-center text-grey-normal', { active: selectedFilter === f.value }]"
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
      <div class="info-row flex justify-between items-center">
          <span class="typography-caption-lg-regular text-blue-custom">{{ pieces }}  قطعه به ارزش تقریبی :</span>
          <span class="typography-body-md-bold text-black">{{ formatNumber(ignotAmount) }} <span class="typography-caption-lg-regular text-white-dark-active">ریال</span></span>
      </div>

      <div v-if="items.length !== 0">
        <!-- cards  -->
          <div class="cards-container full-width">
            <MobileCards
              v-for="(item, index) in items"
              :key="index"
              :image="[item.image]"
              :title="item.title"
              :ayar="item.ayar"
              :price="item.price"
              :discountPrice="item.discountPrice"
              :bestSelling="item.bestSelling"
              :discount="item.discount"
              :PendingDelivery="item.PendingDelivery"
              @click="handleCardRoute(item)"
              class="cursor-pointer"
            />
          </div>
      </div>
      <div v-else>
        <EmptyStatesComponent
          title="دارایی وجود ندارد!!!"
          icon="empty-shop-products"
        />
      </div>
    </div>

  </q-page>
</template>

<script setup>
import MobileCards from 'src/components/MobileCards.vue';
import SvgIcon from 'src/components/SvgIcon.vue';
import { useRouter } from 'vue-router';
import { computed, onMounted, ref, watch } from 'vue';
import { useProductStore } from 'src/stores/productWalletStore';
import { formatNumber } from 'src/utils/Format';
import EmptyStatesComponent from 'src/components/EmptyStatesComponent.vue';

const selectedFilter = ref('all')
const router = useRouter()
const productStore = useProductStore()

const items = computed(() => productStore.items)
const filters = [
  { label: 'همه', value: 'all' },
  { label: 'دارایی طلا', value: 'طلا' },
  { label: 'دارایی نقره',value: 'نقره' },
  { label: 'دارایی شمش', value: 'شمش' }
]

watch(selectedFilter, (newFilter) => {
  productStore.fetchProducts(newFilter)
})

function handleCardRoute(item){
  router.push({
    name:'product-details',
    params: {id: item.id},
  })
}



const pieces = computed(() => productStore.items.length)
const ignotAmount = computed(() => productStore.ignotAmount)

onMounted(() => {
  productStore.fetchProducts(selectedFilter.value)
})

</script>

<style scoped>
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

.main-container-shop {
  padding: 1rem 0.9375rem 4.375rem 1.0625rem; /* 22px 15px 70px 17px */
}

.cards-container {
  display: grid;
  gap: 0.75rem; /* 12px */
  grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr)); /* 160px */
  margin-top: 0.625rem; /* 10px */
}
</style>

