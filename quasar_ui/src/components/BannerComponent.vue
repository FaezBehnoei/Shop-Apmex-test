<template>
  <div class="bg-white-light flex banner">
    <!-- image  -->
     <div>
      <img :src="image" alt="gold-image" />
     </div>
    <!-- title & link  -->
     <div class="title-div flex column justify-evenly ">
      <p class="typography-h4-medium text-black-title q-mb-xs">{{ title }}</p>
      <div class="flex items-center">
        <p class="typography-body-lg-regular text-center q-mb-none q-ml-sm text-white-dark-active">{{ titleLink }}</p>
        <SvgIcon name="arrow-back-l" state="colored" size="24" />
      </div>
     </div>
  </div>
</template>

<script setup>
import SvgIcon from './SvgIcon.vue';

defineProps({
  image:String,
  title: String,
  titleLink: String,
})
</script>

<style scoped>
.banner {
  width: 22.9375rem;       /* 367px */
  height: 8.375rem;        /* 134px */
  border-radius: 0.5rem;   /* 8px */
  gap: 1rem;               /* 16px */
}

.title-div {
  padding: 2.3125rem 0.0625rem 2.3125rem 2.0625rem;  /* 37px 1px 37px 33px */
}
</style>

