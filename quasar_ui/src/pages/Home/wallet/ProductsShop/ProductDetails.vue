<template>
  <q-page class="main-container flex" v-if="selectedItem">
    <!-- img  -->
     <div class="header-padding flex full-width">
      <!-- number  -->
      <div>
        <div v-if="selectedItem?.method === 'inPerson'" class="typography-body-lg-bold text-blue-custom q-mb-xs">در انتظار تحویل حضوری</div>
        <div v-if="selectedItem?.method === 'byPost'" class="typography-body-lg-bold text-blue-custom q-mb-xs">در انتظار تحویل با پیک</div>
        <div class="typography-body-md-medium text-grey-label">شماره سفارش : <span class="typography-body-lg-bold custom-green-number">{{ selectedItem.orderNumber }}</span></div>
      </div>
      <!-- Carosel  -->
      <div class="flex flex-center full-width">
        <ProductIMGcarousel v-if="selectedItem"   :slides="normalizeImages(selectedItem.image, selectedItem.title)"
          :auto-play="true" :auto-play-interval="2000" />
      </div>
     </div>

     <!-- context  -->
      <div class="gold-receipt-page">

        <!-- Purchase details -->
        <div class="purchase-details">
          <!-- Header with amount -->
          <div class="amount-header flex justify-between items-center">
            <div class="product-title text-right">
              <span class="typography-body-lg-bold">{{ selectedItem.title }}</span>
            </div>
            <div class="amount-value  text-left">
              <span class="typography-body-md-bold q-ml-xs">{{ formatNumber(selectedItem.currentPrice) }}</span>
              <span class="typography-caption-md-regular">تومان</span>
            </div>
          </div>
          <div class="purchase-details-container">
          <div class="details-row">
            <!-- Purchase Date Column -->
            <div class="detail-column flex flex-center">
              <div class="column-header typography-caption-lg-regular">تاریخ خرید</div>
              <div class="column-value typography-caption-lg-bold">{{ selectedItem.date }}</div>
            </div>

            <!-- Purchase Price Column -->
            <div class="detail-column">
              <div class="column-header typography-caption-lg-regular">قیمت خرید شما</div>
              <div class="column-value flex flex-center">
                <span class="typography-caption-lg-bold">{{ formatNumber(selectedItem.price) }}</span>
                <span class="currency">تومان</span>
              </div>
            </div>

            <!-- Profit/Loss Column -->
            <div class="detail-column">
              <div class="column-header typography-caption-lg-regular">سود و زیان</div>
              <div class="column-value profit typography-caption-lg-bold">
                <span :class="selectedItem?.profit >= 0 ? 'text-positive' : 'text-negative'" class="typography-caption-lg-bold flex flex-center">
                  <span class="flex flex-center">٪</span>{{ Math.abs(selectedItem?.profit) }}
                  <SvgIcon v-if="selectedItem?.profit >= 0" name="arrow-up" state="black" size="16" />
                  <SvgIcon v-else name="arrow-down" state="red" size="16" />
                </span>
              </div>
            </div>
          </div>
        </div>
        </div>

        <!-- Download invoice button -->
        <div class="download-section flex justify-start">
          <button flat class="download-btn text-primary">
            <SvgIcon name="downloadfactor" state="black" size="16" />
            <span class="text-primary q-mr-xs typography-body-md-medium">دانلود فاکتور خرید</span>
          </button>
        </div>

        <!-- Product description -->
        <div class="product-description text-right">
          <div class="description-title text-right typography-body-md-medium q-mb-xs">توضیحات</div>
          <p class="description-text text-white-darker typography-caption-lg-regular">
            شمش طلای محمدی، نماد اصالت، اعتماد و سرمایه‌گذاری هوشمندانه
            است. این برند با تکیه بر سالها تجربه در صنعت طلا و فلزات گرانبها،
            توانسته است جایگاهی قابل اعتماد در میان فعالان بازار طلا و
            سرمایه‌گذاران حرفه‌ای پیدا کند.
          </p>
        </div>

        <!-- Action buttons -->
        <div class="action-buttons  row q-col-gutter-md">
          <div class="col-6" >
            <ButtonComponent label="فروش به گلدیس" class="full-width custom-btn-recieve "/>
          </div>
          <div class="col-6">
            <ButtonComponent @click="handleDeliveryBtn" :label="btnLabel" class="full-width custom-btn-sell"/>
          </div>
        </div>
      </div>
      <DeliveryMethodDialog v-model:modal-value="openDialog"/>
      <DeliveryInPersonDetailsDialog v-if="address" v-model:modal-value="openDialogInPerson" :address="address" :timing="dateAndtime"/>
      <DeliveryByPostFinalReciptDialog v-if="address" v-model:modal-value="openDialogBypost" :address="address" :timing="dateAndtime" :phone="postPhone"/>

  </q-page>
</template>

<script setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue';
import { usePageTitle } from 'src/composable/usePageTitle';
import { useRoute } from 'vue-router';
import ProductIMGcarousel from 'src/components/ProductIMGcarousel.vue';
import { formatNumber } from 'src/utils/Format';
import SvgIcon from 'src/components/SvgIcon.vue';
import ButtonComponent from 'src/components/ButtonComponent.vue';
import DeliveryMethodDialog from 'src/components/Delivery/DeliveryMethodDialog.vue';
import DeliveryInPersonDetailsDialog from 'src/components/Delivery/DeliveryInPersonDetailsDialog.vue';
import DeliveryByPostFinalReciptDialog from 'src/components/Delivery/DeliveryByPostFinalReciptDialog.vue';
import { useProductStore } from 'src/stores/productWalletStore';

const productStore = useProductStore()
const route = useRoute()

const openDialog = ref(false)
const openDialogInPerson = ref(false)
const openDialogBypost = ref(false)

const address = computed(() => selectedItem.value?.delivery || '')
const dateAndtime = computed(() => selectedItem.value?.delivery?.timing || {})
const postPhone = computed(() => selectedItem.value?.delivery?.phone)


const selectedItem = computed(() => productStore.selectedProduct?.[0])
const btnLabel = computed(() => selectedItem.value.method ? 'جزییات تحویل' : 'دریافت')

function normalizeImages(imageInput, altText = '') {
  if (!imageInput) return []

  if (Array.isArray(imageInput)) {
    return imageInput.map(img => ({ image: img, alt: altText }))
  }

  return [{ image: imageInput, alt: altText }]
}


function handleDeliveryBtn(){
  if(selectedItem.value.method === 'inPerson'){
    openDialogInPerson.value = true
  }else if(selectedItem.value.method === 'byPost'){
    openDialogBypost.value = true
  }else{
    openDialog.value = true
  }
}
watch(
  () => route.params.id,
  (id) => {
    if (id) {
      productStore.fetchProductByIdWallet(parseInt(id))
    }
  },
  { immediate: true }
)

watch(
  () => selectedItem.value?.title,
  (title) => {
    if (title) usePageTitle(title)
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  openDialog.value = false
  openDialogBypost.value = false
  openDialogInPerson.value = false
})

</script>

<style scoped>
.main-container{
  padding-bottom: 2px;
}

.header-padding {
  background-color: rgba(247, 247, 247, 1);
  padding: 1rem 1rem;
}

.gold-receipt-page {
  padding: 1.5rem 1rem;
  background-color: white;
  width: 100%;
  border-top-left-radius: 2.5rem;  /* 40px */
  border-top-right-radius: 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1.5rem;
  margin-top: -2rem;
}

.amount-header {
  padding-bottom: 1.5rem;
}

.border-top {
  border-top: 1px solid #f0f0f0;
}

.amount-value {
  color: var(--orange-primary);
}

.description-text {
  margin-bottom: 0;
  text-align: justify;
}

.action-buttons {
  margin-top: 0; /* 36px */
}

.action-btn {
  border-radius: 0.5rem; /* 8px */
  height: 3rem;           /* 48px */
}

.download-btn {
  outline: none;
  border: none;
  background-color: transparent;
  display: flex;
  align-items: center;
  color: rgba(45, 156, 219, 1);
}

.detail-row {
  padding: 0.5rem 0; /* 8px 0 */
}

.text-positive {
  color: #21BA45;
}

.purchase-details-container {
  background-color: #f8f8f8;
  border-radius: 0.5rem; /* 8px */
  padding: 0.5rem 1rem;
  width: 100%;
}

.details-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.detail-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.column-header {
  color: rgba(89, 89, 89, 1);
  white-space: nowrap;
}

.column-value {
  white-space: nowrap;
}

.currency {
  font-size: 0.75rem;  /* 12px */
  margin-right: 0.125rem; /* 2px */
}

.profit {
  color: #d32f2f;
}

.custom-btn-recieve {
  background-color: rgba(102, 191, 161, 1);
  color: white;
  font-weight: 500;
  font-size: 0.875rem;     /* 14px */
  line-height: 1.375rem;   /* 22px */
  letter-spacing: 0%;
}

.custom-btn-sell {
  background-color: white;
  color: rgba(102, 191, 161, 1);
  border: 1px solid rgba(102, 191, 161, 1);
  font-weight: 500;
  font-size: 0.875rem;     /* 14px */
  line-height: 1.375rem;   /* 22px */
  letter-spacing: 0%;
}

.custom-green-number {
  color: rgba(102, 191, 161, 1);
}
</style>

