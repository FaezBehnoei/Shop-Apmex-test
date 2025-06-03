<template>
  <div class="custom-carousel-container">
    <div class="carousel-track" v-if="slides && slides.length" :style="{ transform: `translateX(${currentSlide * 100}%)` }">
      <div v-for="(slide, index) in slides" :key="index" class="carousel-slide">
        <div class="image-wrapper">
          <img :src="slide.image" :alt="slide.alt" class="product-image" />
        </div>
      </div>
    </div>

    <div class="carousel-arrows" v-if="showArrows">
      <button class="arrow prev" @click="prevSlide">&lt;</button>
      <button class="arrow next" @click="nextSlide">&gt;</button>
    </div>

    <div class="carousel-indicators" v-if="slides && slides.length > 1">
      <span
        v-for="(slide, index) in slides"
        :key="index"
        class="indicator"
        :class="{ active: currentSlide === index }"
        @click="goToSlide(index)"
      ></span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  slides: {
    type: [Array, String],
    required: true,
  },
  autoPlay: {
    type: Boolean,
    default: true,
  },
  autoPlayInterval: {
    type: Number,
    default: 5000,
  },
  showArrows: {
    type: Boolean,
    default: false,
  },
});



const currentSlide = ref(0);
let autoPlayTimer = null;

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % props.slides.length;
};

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + props.slides.length) % props.slides.length;
};

const goToSlide = (index) => {
  currentSlide.value = index;
  resetAutoPlay();
};

const startAutoPlay = () => {
  if (props.autoPlay) {
    autoPlayTimer = setInterval(() => {
      nextSlide();
    }, props.autoPlayInterval);
  }
};

const stopAutoPlay = () => {
  clearInterval(autoPlayTimer);
  autoPlayTimer = null;
};

const resetAutoPlay = () => {
  stopAutoPlay();
  startAutoPlay();
};

onMounted(() => {
  startAutoPlay();
  console.log(props.slides)
});
onBeforeUnmount(() => {
  stopAutoPlay();
});
</script>

<style scoped>
.custom-carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  background-color: transparent;
  border-radius: 0.5rem; /* 8px */
  margin-bottom: 1rem;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease;
  width: 100%;
}

.carousel-slide {
  min-width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}
.image-wrapper {
  width: 17.18rem;      /* یا مثلا 40vw برای ریسپانسیو‌تر */
  height: 13.62rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  margin-bottom: 1rem;
}

.carousel-indicators {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.25rem; /* 4px */
  position: absolute;
  bottom: 0.625rem; /* 10px */
  width: 100%;
}

.indicator {
  width: 0.375rem; /* 6px */
  height: 0.375rem;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.indicator.active {
  width: 0.5rem; /* 8px */
  height: 0.5rem;
  background-color: #FD7E14;
}

.carousel-arrows {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.arrow {
  background-color: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 50%;
  width: 1.875rem; /* 30px */
  height: 1.875rem;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  font-size: 1.125rem; /* 18px */
  margin: 0 0.625rem; /* 10px */
  transition: background-color 0.3s ease;
}

.arrow:hover {
  background-color: rgba(255, 255, 255, 0.9);
}
</style>

