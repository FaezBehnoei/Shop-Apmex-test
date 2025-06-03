
<template>
  <div class="main-container ">
    <div class="content-wrapper q-mx-auto">
      <!-- title & icons  -->
      <div class="flex justify-between items-center q-mb-md">
        <!-- title  -->
        <div class="flex items-center">
          <span class="typography-h3-bold text-blue-dark q-ml-md">{{ title }}</span>
          <span class="typography-body-lg-medium text-orange-primary q-pa-xs">مشاهده همه</span>
          <SvgIcon name="arrow-back-m" state="colored" size="16" />
        </div>
        <!-- icons  -->
          <div class="flex items-cneter justify-between navigation-btn">
            <button @click="goPrev" :disabled="currentPage === 0">
              <SvgIcon  class="q-ml-sm" name="chevron-right" state="colored" size="24"/>
            </button>
            <button @click="goNext" :disabled="currentPage >= totalPages - 1">
              <SvgIcon  class="q-mr-sm" name="chevron-left" state="colored" size="24"/>
            </button>
          </div>
      </div>
      <!-- cards  -->
      <div class="carousel-container">
        <div class="carousel-track"
        :style="{ transform: `translateX(${direction === 'rtl' ? slideOffset : -slideOffset}px)` }"

        >
          <div v-for="(item, index) in props.card" :key="index" class="carousel-item">
            <CardComponent
            class="bg-white "
            v-bind="item"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup >
import { computed,ref, watch,onMounted } from 'vue';
import CardComponent from './CardComponent.vue';
import SvgIcon from './SvgIcon.vue';

const props = defineProps({
  card:Object,
  title: String,
  direction:{
    type: String,
    default: 'rtl'
  }
})
const currentPage = ref(0)
const cardPerPage = ref(4)
const slideOffset = ref(0);
const itemWidth = ref(0);
const containerWidth = ref(0)

onMounted(() => {
  calculateDimensions();
  window.addEventListener('resize', calculateDimensions);
});

const calculateDimensions = () => {
  const container = document.querySelector('.carousel-container')
  if(container){
    containerWidth.value = container.offsetWidth;
    itemWidth.value = containerWidth.value / cardPerPage.value;
    updateSlideOffset()
  }
}

watch(currentPage, () => {
  updateSlideOffset()
})

const updateSlideOffset = () => {
  slideOffset.value = currentPage.value * containerWidth.value;
};



const totalPages = computed(() => Math.ceil(props.card.length / cardPerPage.value))



const goNext = () => {
  if (currentPage.value < totalPages.value - 1) {
    currentPage.value++
  }
}

const goPrev = () => {
  if (currentPage.value > 0) {
    currentPage.value--
  }
}

</script>

<style scoped>
.main-container {
  padding: 1.5rem 9.375rem 3.375rem 9.375rem; /* 24px 150px 54px 150px */
  background-color: rgba(242, 244, 253, 1);
  width: 100vw;
}

.content-wrapper {
  max-width: 71.25rem; /* 1140px */
  display: flex;
  flex-direction: column;
  gap: 1rem; /* 16px */
}

.navigation-btn button {
  background: none;
  outline: none;
  border: none;
}

.navigation-btn:disabled {
  cursor: not-allowed;
}

.carousel-container {
  position: relative;
  overflow: hidden;
  width: 100%;
}

.carousel-track {
  display: flex;
  transition: transform 0.8s ease;
  width: 100%;
}

.carousel-item {
  flex: 0 0 25%; /* 4 items per page */
  box-sizing: border-box;
}
</style>

