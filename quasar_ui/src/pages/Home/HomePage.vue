<template>
  <q-page class="q-pt-sm custom-padding-home">


    <!-- sub header  -->
    <div class="metal-scroll-container">
      <div
        v-for="metal in homeStore.metals"
        :key="metal.title"
        class="metal-card"
      >
        <div class="metal-name typography-caption-md-regular">{{ metal.title }}</div>
        <div class="metal-price-row">
          <span class="metal-price typography-caption-lg-medium ">{{ formatNumber(metal.price) }} <span class="typography-caption-md-regular">تومان</span></span>
          <span
            class="metal-change flex flex-center typography-caption-md-bold"
            :class="{
              'positive': metal.change > 0,
              'negative': metal.change < 0
            }"
          >
            {{ Math.abs(metal.change).toFixed(2) }}٪
            <SvgIcon v-if="metal.change > 0" name="arrow-up" state="black" size="16" />
            <SvgIcon v-if="metal.change < 0" name="arrow-down" state="red" size="16" />
          </span>
        </div>
      </div>
    </div>

    <!-- order Card  -->
    <div v-if="isOrdered" class="order-card-wrapper">
      <OrderCard class="cursor-pointer" v-for="item in homeStore.orders" :key="item.id" :order="item" @click="handleOpenProductPage(item)"/>
    </div>

     <!-- banner -->
    <div v-if="!isOrdered" class="banner-container">
      <BannerDashboard />
    </div>

    <!-- slider -->
    <DashboardContainer
      title="دسته بندی محصولات"
      :items="homeStore.categories"
      show-more-route="/products/best"
      :card-component="ignotsCartDashboard"
    />

    <!-- slider -->
    <DashboardContainer
      title="پرفروش‌ترین‌ ها"
      :items="homeStore.bestSellers"
      show-more-route="/products/best"
      :card-component="CardProductsDashboard"
    />

    <!-- banner -->
    <div v-if="isOrdered" class="banner-container">
      <BannerDashboard />
    </div>

    <!-- chart Component -->
    <div class="q-pa-md">
      <div class="section-header flex justify-between items-center q-mb-md">
        <div class="typography-body-md-bold text-blue-custom">نمای کلی</div>
        <router-link :to="showMoreRoute" class="view-more-link flex flex-center typography-caption-md-regular">
          مشاهده نمودار ها <span class="flex items-center ">
            <SvgIcon class="q-mr-xs" name="arrow-back-xs" state="colored" size="14"/>
          </span>
        </router-link>
      </div>

      <ChartComponentDashboard
      v-if="homeStore.chart && Object.keys(homeStore.chart).length"
      :data="homeStore.chart.data"
      :timestamps="homeStore.chart.timestamps"
      :profit-indicators="homeStore.chart.profit_indicators"
    />



    </div>
    <!-- slider -->
    <DashboardContainer
      title="اخبار"
      :items="homeStore.news"
      show-more-route="/products/best"
      :card-component="NewsDashboardComponent"
      :is-column="true"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useHomeStore } from 'stores/homeDashboardStore'
import BannerDashboard from 'src/components/Home/bannerDashboard.vue'
import CardProductsDashboard from 'src/components/Home/cardProductsDashboard.vue'
import ChartComponentDashboard from 'src/components/Home/chartComponentDashboard.vue'
import DashboardContainer from 'src/components/Home/dashboardContainer.vue'
import ignotsCartDashboard from 'src/components/Home/ignotsCartDashboard.vue'
import OrderCard from 'src/components/Home/orderCard.vue'
import SvgIcon from 'src/components/SvgIcon.vue'
import { formatNumber } from 'src/utils/Format'
import NewsDashboardComponent from 'src/components/Home/newsDashboardComponent.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const homeStore = useHomeStore()
const showMoreRoute = '/dashboard/charts'
const isOrdered = computed(() => homeStore.orders ? true : false)

onMounted(() => {
  homeStore.fetchAllDashboardData()
})

async function handleOpenProductPage(item){
  router.push({
    name:'product-details',
    params: {id: item.id},
  })
}
</script>

<style scoped>

.metal-scroll-container {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  padding: 0.5rem 1rem;
}

.metal-scroll-container::-webkit-scrollbar {
  display: none;
}

.metal-card {
  flex: 0 0 auto;
  background: rgba(247, 247, 247, 1);
  padding: 0.5rem;
  border-radius: 0.5rem;
  border: 1px solid #f0f0f0;
  text-align: right;
}

.metal-price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  direction: rtl;
}
.metal-name{
  color: rgba(49, 49, 49, 1);
}

.metal-change {
  padding: 2px 6px;
  border-radius: 4px;
}

.metal-change.positive {
  color: #22A958;
}

.metal-change.negative {
  color: #EF4444;
}

.order-card-wrapper {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding: 1rem;
  scrollbar-width: none; /* for Firefox */
}

.order-card-wrapper::-webkit-scrollbar {
  display: none; /* for Chrome & Safari */
}


.banner-container{
  padding: 0.5rem 1rem;
  box-shadow: none;
}

.section-header .view-more-link {
  color: var(--orange-primary);
}
.custom-padding-home{
  padding-bottom: 4rem;
}
</style>
