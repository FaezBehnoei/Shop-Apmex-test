<template>
  <div class="section-wrapper">
    <!-- Header -->
    <div class="section-header flex justify-between items-center q-px-sm q-mb-sm">
      <div class="typography-body-md-bold text-blue-custom">{{ title }}</div>
      <router-link :to="showMoreRoute" class="view-more-link flex flex-center typography-caption-md-regular">{{ showMoreText }} <span class="flex items-center ">
        <SvgIcon  class="q-mr-xs" name="arrow-back-xs" state="colored" size="14"/>
      </span></router-link>
    </div>

    <!-- Horizontal Scroll -->
    <div class="product-scroll-container" :class="isColumn ? 'column q-gutter-y-sm' : ''">
      <component
        :is="cardComponent"
        v-for="item in props.items"
        :key="item.id"
        v-bind="item"
      />
    </div>
  </div>
</template>


<script setup>
import SvgIcon from '../SvgIcon.vue';
const props = defineProps({
  title: String,
  items: Array,
  showMoreText: {
    type: String,
    default: 'مشاهده همه'
  },
  showMoreRoute: {
    type: String,
    default: '/'
  },
  cardComponent: {
    type: [Object, String],
    required: true
  },
  itemProps: {
    // Function to customize the props passed to each card
    type: Function,
    default: (item) => ({ product: item })
  },
  isColumn: Boolean
})
</script>

<style scoped>
.section-wrapper {
  padding: 0.5rem 1rem;
}

.section-header .view-more-link {
  color: var(--orange-primary);
}

.product-scroll-container {
  display: flex;
  gap: 0.75rem;
  padding: 0.5rem 0;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.product-scroll-container > * {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
}


.product-scroll-container::-webkit-scrollbar {
  display: none;
}

</style>
