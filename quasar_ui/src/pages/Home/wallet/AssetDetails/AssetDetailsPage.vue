<template>
  <q-page class="q-mb-md">
    <!-- top card -->
    <div class="flex column q-px-md q-mb-md" :class="expanded ? 'expanded' : ''">
      <!-- دارایی section -->
      <div class="flex items-center justify-between q-mb-md">
        <div class="typography-caption-lg-regular text-blue-custom flex items-center">
          <div :style="{ backgroundColor: asset?.color }" class="gold-icon q-ml-xs"></div>
          دارایی {{ store.asset?.name }} :
        </div>
        <div>
          <span class="typography-body-md-bold text-black">{{ asset?.amount }}</span>
          <span class="typography-caption-lg-regular text-white-dark-active q-mr-sm">{{ asset?.unit }}</span>
        </div>
      </div>

      <!-- سود و زیان section -->
      <div class="flex items-center justify-between">
        <div class="typography-caption-lg-regular text-blue-custom">
          سود و زیان شما تا به این لحظه :
        </div>
        <div class="flex items-center">
          <span :class="asset?.profit_percent >= 0 ? 'text-positive' : 'text-negative'" class="typography-caption-lg-regular q-ml-sm">
            {{ Math.abs(asset?.profit_percent) }}٪
            <SvgIcon v-if="asset?.profit_percent >= 0" name="arrow-up" state="black" size="16" />
            <SvgIcon v-else name="arrow-down" state="red" size="16" />
          </span>
          <span class="typography-body-md-bold text-black">{{ formatNumber(asset?.profit_amount) }}</span>
          <span class="typography-caption-lg-regular text-white-dark-active q-mr-xs">ریال</span>
        </div>
      </div>
    </div>

    <!-- chart -->
    <div class="q-pt-sm q-px-md">
      <div class="typography-body-md-bold text-blue-custom q-mb-md">نمودار سود دهی شما</div>
      <ChartComponent
        :data="chartData"
        :timestamps="timesstamps"
        :color="store.asset?.color"
        :profit-indicators="store.profitIndicators"
      />

      <div class="typography-body-md-bold text-blue-custom q-mb-sm">تاریخچه تراکنش ها</div>

      <div class="custom-margin">
        <div v-for="tx in transactions" :key="tx.id" class="transaction-content">
          <div class="transaction-left">
            <div class="flex items-center">
              <div class="transaction-amount flex items-center q-mb-md">
                <span class="amount-value typography-body-md-regular text-blue-custom">{{ tx.amount }}</span>
                <span class="amount-currency typography-caption-md-regular text-white-dark-hover q-pr-xs">{{ asset?.unit }}</span>
                <div class="transaction-type typography-body-md-regular text-blue-custom q-mr-sm" :class="tx.typeColor">
                  {{ tx.type }}
                </div>
              </div>
            </div>
            <div class="transaction-time typography-caption-md-regular text-white-dark-hover">
              {{ tx.date }}<span class="q-px-xs">-</span>{{ tx.time }}
            </div>
          </div>

          <div class="transaction-right">
            <div class="transaction-status typography-caption-md-regular" :class="tx.status === 3 ? 'success' : tx.status === 2 ? 'pending' : 'failed'">
              {{ tx.statusText }}
            </div>
            <div class="transaction-more">
              <span class="more-text typography-caption-md-regular text-black-custom">بیشتر</span>
              <SvgIcon name="arrow-left" state="black" size="16" />
            </div>
          </div>
        </div>
      </div>

      <div class="row q-col-gutter-sm q-pb-xl">
        <div class="col-6 text-center">
          <ButtonComponent @click="router.push(`/account/buy/${asset?.slug}`)" size="lg" label="خرید" type="primary" class="full-width sell-button" />
        </div>
        <div class="col-6 text-center">
          <ButtonComponent @click="router.push(`/account/sell/${asset?.slug}`)" size="lg" label="فروش" type="stroke" class="custom-bg sell-button full-width" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SvgIcon from 'src/components/SvgIcon.vue'
import ChartComponent from 'src/components/ChartComponent.vue'
import ButtonComponent from 'src/components/ButtonComponent.vue'
import { useAssetDetailStore } from 'src/stores/assetdetailsStore'
import { formatNumber } from 'src/utils/Format'

const route = useRoute()
const router = useRouter()
const store = useAssetDetailStore()
const expanded = ref(false)


const chartData = computed(() => store.rawChartData)
const timesstamps = computed(() => store.timestamps)


const asset = computed(() => store.asset)
const transactions = computed(() => store.transactions)
const selectedRange = ref('24h')
const fetchAssetDetail = store.fetchAssetDetail

watch(selectedRange, (newRange) => {
  store.selectedRange = newRange
})


onMounted(async() => {
  const assetSlug = route.params.type
  await fetchAssetDetail(assetSlug)
})
</script>

<style scoped>
/* تمام استایل‌های قبلیت اینجا بدون تغییر قابل استفاده‌اند */
.gold-icon {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 0.09375rem;
  background-color: red;
}
.transaction-content {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  align-items: center;
  background-color: var(--white-light-active);
}
.transaction-left {
  display: flex;
  flex-direction: column;
}
.transaction-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.transaction-status {
  padding: 0.125rem 0.5rem; /* 2px 8px */
  border-radius: 0.25rem;   /* 4px */
  margin-bottom: 1rem;      /* 16px */
}
.transaction-more {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.transaction-status.success {
  color: var(--q-positive);
}
.transaction-status.failed {
  color: var(--q-negative);
}
.transaction-status.pending {
  color: var(--orange-primary);
}
.custom-margin {
  margin-bottom: 4rem;
}
.sell-button {
  padding-inline: 0;
}
</style>
