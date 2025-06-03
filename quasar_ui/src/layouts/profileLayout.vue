<template>
  <q-layout view="lHh Lpr lFf">

    <!-- header  -->
     <div class="flex items-center page-header">
      <button @click="router.back()" class="back-btn">
        <SvgIcon class="back-icon" name="navbar-up" state="black" size="24"  cursor="true"/>
      </button>
      <div class="full-width text-center">
          <span class="typography-body-lg-bold flex flex-center text-black">{{ title }}</span>
        </div>
      </div>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import SvgIcon from 'src/components/SvgIcon.vue';
import { computed } from 'vue';

const router = useRouter()
const route = useRoute()
const title = computed(() => route.meta.title)
</script>

<style scoped>
.page-header {
  position: relative;
  height: 3rem;           /* 48px */
  padding: 0 1rem;        /* 16px */
  margin-bottom: 1rem;
}

.page-header .back-icon {
  position: absolute;
  right: 1rem;            /* 16px */
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.back-btn {
  outline: none;
  border: none;
}

</style>
