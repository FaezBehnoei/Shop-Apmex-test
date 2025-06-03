<template>
  <div class="main-card">
    <!-- badge  -->
    <div  v-if="bestSelling"  class="banner-badge">
      <span class="typography-caption-lg-bold text-white">پرفروش ترین </span>
    </div>
    <div v-if="discount" class="discount-badge flex flex-center">
      <span class="typography-body-lg-medium text-white text-center">{{ discount }}%</span>
    </div>

    <!-- main content  -->
     <div class="main-content">
      <!-- image  -->
       <div class="flex flex-center q-mb-md">
        <img :src="image" :alt="title">
       </div>
       <!-- content  -->
      <div>
        <div>
          <p class="typography-body-lg-bold q-mb-sm">{{ title }}</p>
        </div>
        <div class="flex items-center justify-between">
          <span class="typography-body-lg-regular text-grey-dark q-mb-sm">عیار:</span>
          <span class="typography-body-lg-regular text-grey-dark">{{ ayar }}</span>
        </div>
        <div class="flex items-start justify-between">
          <div>
            <span class="typography-body-lg-regular text-grey-dark">قیمت:</span>
          </div>
          <div class="flex column">
            <span class="typography-body-lg-regular text-grey-dark">{{ price }} تومان</span>
            <span class="typography-body-lg-regular color-text text-strike">{{ discountPrice }} </span>
          </div>
        </div>
      </div>
     </div>
  </div>
</template>

<script setup>
defineProps({
  image:String,
  title: String,
  ayar: Number,
  price: Number,
  bestSelling: Boolean,
  discount: Number,
  discountPrice: Number
})
</script>

<style scoped>
.main-card {
  width: 17.0625rem; /* 273px */
  height: 22.4375rem; /* 359px */
  border-radius: 0.5rem; /* 8px */
  padding-top: 3.25rem; /* 52px */
  padding-right: 1rem; /* 16px */
  padding-bottom: 2.75rem; /* 44px */
  padding-left: 1rem; /* 16px */
  border: 1px solid rgba(212, 212, 212, 1);
  position: relative;
}

.banner-badge {
  width: 5.5rem; /* 88px */
  padding: 0.375rem 0.625rem; /* 6px 10px */
  border-top-right-radius: 0.5rem; /* 8px */
  background-color: rgba(255, 127, 62, 1);
  position: absolute;
  top: 0;
  right: 0;
}

.discount-badge {
  width: 2.25rem; /* 36px */
  height: 2.25rem; /* 36px */
  background-color: rgba(255, 24, 24, 1);
  border-radius: 0.5rem; /* 8px */
  padding: 0.5rem 0.625rem; /* 8px 10px */
  position: absolute;
  top: 1rem; /* 16px */
  left: 1rem; /* 16px */
}

.color-text {
  color: rgba(217, 217, 217, 1);
}
</style>

