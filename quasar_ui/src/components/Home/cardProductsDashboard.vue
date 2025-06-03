<template>
  <div class="main-card">
    <!-- badge  -->
    <div  v-if="bestSelling"  class="banner-badge">
      <span class="typography-caption-lg-bold text-white">پرفروش ترین </span>
    </div>
    <div v-if="discount" class="discount-badge flex flex-center">
      <span class="typography-body-lg-medium text-white text-center">{{ discount }}%</span>
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
        <div class="flex justify-end">
          <div class="flex column">
            <span class="typography-caption-md-regular color-text"><span class="typography-body-lg-bold">{{ formatNumber(price) }}</span> تومان</span>
            <span v-if="discountPrice" class="typography-caption-md-regular text-strike">{{ discountPrice }} </span>
          </div>
        </div>
      </div>
     </div>
  </div>
</template>

<script setup>
import { formatNumber } from 'src/utils/Format';
defineProps({
  image:String,
  title: String,
  ayar: Number,
  price: Number,
  bestSelling: Boolean,
  discount: Number,
  discountPrice: Number,
  PendingDelivery: Boolean
})
</script>

<style scoped>
.main-card {
  background-color: var(--white-light);
  border: 1px solid var(--white-light-active);
  padding: 0.1rem 0.5rem 0.5rem 0.5rem;
  border-radius: 0.5rem; /* 8px */
  position: relative;
  width: 100%;
}

.banner-badge {
  border-top-right-radius: 0.5rem; /* 8px */
  background-color: rgba(255, 127, 62, 1);
  position: absolute;
  top: 0;
  right: 0;
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
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 40vw;
  max-height: 40vh;
}
.product-img{
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
