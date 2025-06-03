<template>
  <div class="carousel-container">
    <div class="carousel-track"
        :style="{ transform: `translateX(${direction === 'rtl' ? slideOffset : -slideOffset}px)` }"

      >
      <div v-for="(slide, index) in slides"
      :key="index"
       class="carousel-item"
      >
      <img :src="slide.img" alt="images" />
      </div>
    </div>
      <div class="dots">
        <span
          v-for="(_, i) in slides"
          :key="i"
          :class="['dot', { active: i === currentIndex }]"
          @click="goTo(i)"
        ></span>
      </div>
  </div>
</template>

<script setup>
import { ref,watch, onMounted } from 'vue';

const slides = ref([
  {id:1, img:'/images/carouselLogin1.png'},
  {id:2, img:'/images/carouselLogin2.png'},
  {id:3, img:'/images/carouselLogin3.png'},
])

const currentPage = ref(0)
const cardPerPage = ref(1)
const slideOffset = ref(0);
const itemWidth = ref(0);
const containerWidth = ref(0)

const calculateDimensions = () => {
  const container = document.querySelector('.carousel-container')
  if(container){
    containerWidth.value = container.offsetWidth;
    itemWidth.value = containerWidth.value / cardPerPage.value;
    updateSlideOffset()
  }
}
onMounted(() => {
  calculateDimensions();
  window.addEventListener('resize', calculateDimensions);
});

watch(currentPage, () => {
  updateSlideOffset()
})

const updateSlideOffset = () => {
  slideOffset.value = currentPage.value * containerWidth.value;
};
// const totalPages = computed(() => Math.ceil(slides.value.length / cardPerPage.value))

</script>

<style scoped>
.carousel-container {
  position: relative;
  overflow: hidden;
  width: 100%;
  max-width: 375px;
}

.carousel-track {
  display: flex;
  transition: transform 0.8s ease;
  width: 100%;
}
.carousel-item {
  flex: 1;
  box-sizing: border-box;
}
</style>
