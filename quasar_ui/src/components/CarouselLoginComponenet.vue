<template>
  <div class="carousel-container q-mx-auto">
    <div class="carousel-slides" :style="slideStyle">
      <div class="carousel-slide" v-for="(slide, idx) in slides" :key="idx">
        <img :src="slide.img" alt="img" class="img-slide" />
      </div>
    </div>
    <!-- dots  -->
    <div class="carousel-dots flex items-center">
      <span
        v-for="(slide, idx) in slides"
        :key="idx"
        class="dots"
        :class="dotClass(idx)"
        @click="goToSlide(idx)"
      ></span>
    </div>
    <!-- logo  -->
    <div class="flex custom-margin-logo">
      <img src="/images/monogram_color_2_48px.svg" alt="monogram" class="q-ml-md" :width="48" />
      <img src="/images/logo (1).svg" alt="logo" :width="144" />
    </div>
    <!-- text  -->
    <div class="custom-margin">
      <p class="typography-body-md-regular text-blue-custom">{{ slides[currentIndex].text }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';

let isAutoInterval = null
const slides = ref([
  {id:1, img:'/images/carouselLogin1.svg',text:'گلدیس سیستم پیشرفته‌ی خرید طلای فیزیکی و مقایسه آخرین قیمت فلزات گرانبها با بازار '},
  {id:2, img:'/images/carouselLogin2.svg',text: 'خرید بهترین قیمت شمش طلا و مصنوعات طلا و مقایسه آن با دیگر دیگر محصولات موجود در بازار سرمایه.'},
  {id:3, img:'/images/carouselLogin3.svg',text:'بررسی محصولات و بهترین سرمایه گذاری برروی سکه طلا و مدیریت نقدینگی'},
])

const currentIndex = ref(0)

function goToSlide(idx){
  currentIndex.value = idx
}

// استفاده از translate3d برای بهینه‌سازی GPU
const slideStyle = computed(() => ({
  transform: `translate3d(${currentIndex.value * 100}%, 0, 0)`
}))

function dotClass(idx){
  const distance = Math.abs(currentIndex.value - idx)
  if(distance === 0) return 'dot--active'
  else if (distance === 1) return 'dot--near'
  else return 'dot--far'
}

const next = () => {
  if (currentIndex.value >= slides.value.length - 1) {
    currentIndex.value = 0
  } else {
    currentIndex.value++
  }
}

onMounted(() => {
  isAutoInterval = setInterval(next, 2000)
})

onUnmounted(() => {
  clearInterval(isAutoInterval)
})
</script>

<style scoped>
.carousel-container {
  width: 100%;
  overflow: hidden;
  max-width: 23.4375rem; /* 375px */
  position: relative;
  contain: layout style paint; /* بهینه‌سازی rendering */
}

.carousel-slides {
  display: flex;
  transition: transform 0.5s ease-in-out;
  will-change: transform; /* بهینه‌سازی GPU */
  backface-visibility: hidden; /* جلوگیری از flickering */
  transform-style: preserve-3d; /* حفظ 3D context */
}

.carousel-slide {
  min-width: 100%;
  text-align: center;
  user-select: none;
  transform: translateZ(0); /* فعال‌سازی hardware acceleration */
  backface-visibility: hidden; /* بهینه‌سازی اضافی */
}

.carousel-slide img {
  width: 100%;
  object-fit: contain;
  margin-bottom: 4.0625rem; /* 65px */
  max-height: 45vh;
}

.dots {
  width: 0.75rem; /* 12px */
  height: 0.75rem; /* 12px */
  border-radius: 50%;
  cursor: pointer;
  background-color: #D9D9D9;
  margin-left: 0.375rem; /* 6px */
  transition: all 0.3s ease; /* انیمیشن نرم برای dots */
}

.dot--active {
  width: 1rem; /* 16px */
  height: 1rem; /* 16px */
  background-color: #FF7F33;
}

.dot--near {
  width: 0.875rem; /* 14px */
  height: 0.875rem; /* 14px */
  background-color: #D9D9D9;
}

.dot--far {
  width: 0.75rem; /* 12px */
  height: 0.75rem; /* 12px */
  background-color: #E0E0E0;
}

.custom-margin {
  margin-bottom: 3.375rem; /* 54px */
}

@media (max-height: 700px) {
  .custom-margin {
    margin-bottom: 0;
  }
  .carousel-slide img {
    margin-bottom: 1rem;
  }
}

.carousel-dots {
  height: 2vh;
  margin-bottom: 1.5rem; /* 24px */
}

.custom-margin-logo {
  margin-bottom: 1.5rem; /* 24px */
}

.img-slide {
  max-width: 20rem; /* 320px */
  max-height: 20rem; /* 320px */
}

/* اضافه کردن prefixed properties برای سازگاری بیشتر */
@supports (transform: translate3d(0, 0, 0)) {
  .carousel-slides {
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
  }
}
</style>
