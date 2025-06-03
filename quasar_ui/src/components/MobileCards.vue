<template>
  <div class="main-card">
    <!-- badge  -->
    <div v-if="bestSelling || discount" class="delivery-badge bg-red-5 q-px-sm flex flex-center">
      <span  v-if="bestSelling" class="typography-caption-md-regular text-center">پرفروش ترین </span>
      <span v-else-if="discount" class="typography-caption-lg-regular text-center">{{ discount }}%</span>
    </div>
    <div v-if="PendingDelivery" class="delivery-badge flex flex-center">
      <span class="text-center">در انتظار تحویل</span>
    </div>

    <!-- main content  -->
     <div class="main-content">
      <!-- image  -->
       <div class="image-wrapper">
        <img :src="Array.isArray(image) ? image[0] : image" :alt="title" class="product-img">
       </div>
       <!-- content  -->
      <div>
        <div>
          <p class="typography-caption-lg-regular q-mb-xs">{{ title }}</p>
        </div>
        <div class="flex items-center">
          <span class="typography-caption-lg-regular text-white-darker q-mb-xs">عیار {{  ayar }}</span>
        </div>
        <div class="flex justify-between items-start" :class="{'q-mt-sm' : purchaseShop === true}" >
          <div class="flex flex-center purchase-wrapper"
            :class="{invisible : purchaseShop === false}"
          >
            <SvgIcon name="purchase-shop" state="black" size="16" />
          </div>
          <div class="flex justify-end">
          <div class="flex column justify-end">
            <span :class="{'text-black' : purchaseShop === true}" class="typography-caption-md-regular color-text"><span class="typography-body-lg-bold">{{ formatNumber(price) }}</span> تومان</span>
            <span
              class="typography-caption-lg-regular text-white-dark text-strike fake-discount"
              :class="{ invisible: !discountPrice }"
            >
              <span>{{ formatNumber(discountPrice || price) }}</span>
            </span>
          </div>
        </div>
        </div>
      </div>
     </div>
  </div>
</template>

<script setup>
import { formatNumber } from 'src/utils/Format';
import SvgIcon from './SvgIcon.vue';
defineProps({
  image:Array,
  title: String,
  ayar: Number,
  price: Number,
  bestSelling: Boolean,
  discount: Number,
  discountPrice: Number,
  PendingDelivery: Boolean,
  purchaseShop: Boolean
})
</script>

<style scoped>
.main-card {
  padding: 0.1rem 0.5rem 0rem 0.5rem;
  border-radius: 0.5rem; /* 8px */
  position: relative;
  box-shadow: 0 0.25rem 0.625rem 0 rgba(0, 0, 0, 0.08); /* 4px 10px */
  width: 100%;
}

.banner-badge {
  border-top-right-radius: 0.5rem; /* 8px */
  background-color: rgba(255, 127, 62, 1);
  position: absolute;
  top: 0;
  left: 0;
}

.discount-badge {
  background-color: rgba(255, 24, 24, 1);
  border-radius: 0.5rem; /* 8px */
  position: absolute;
  top: 1rem; /* 16px */
  left: 1rem; /* 16px */
}
.delivery-badge{
  background-color: rgba(102, 191, 161, 1);
  position: absolute;
  top: 0;
  left: 0;
  font-weight: 500;
  font-size: 0.5rem;
  line-height: 0.875rem;
  letter-spacing: 0%;
  color: white;
  border-radius: 0.5rem 0 0.5rem 0 ;
  padding: 0.1875rem 0.125rem;
}

.color-text {
  color: rgba(255, 127, 51, 1);
}
.image-wrapper {
  width: 100%;
  aspect-ratio: 1.2 / 1;
  overflow: hidden;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.product-img{
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.purchase-wrapper{
  background-color: var(--orange-primary);
  padding: 0.25rem;
  border-radius: 4px;
}
.invisible {
  visibility: hidden;
}


</style>
