<template>
  <q-layout view="lHh Lpr lFf" >

    <div v-if="hideHeader && titlePage.title" class="flex items-center page-header">
      <button @click="router.back()" class="back-btn">
        <SvgIcon class="back-icon" name="navbar-up" state="black" size="24"  cursor="true"/>
      </button>
      <div class="full-width text-center">
          <span class="typography-body-lg-bold flex flex-center text-black">{{ titlePage.title }}</span>
        </div>
      </div>


    <q-page-container :class="{ 'main-container': !hideFooter }">
      <router-view />
    </q-page-container>

    <FooterComponent v-if="!hideFooter" />
  </q-layout>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import { usePageTitle } from 'src/composable/usePageTitle';

import FooterComponent from 'src/components/FooterComponent.vue';
import SvgIcon from 'src/components/SvgIcon.vue';

const router = useRouter()
const route = useRoute()

const hideHeader = computed(() => {
  return route.meta.hideHeader === true;
})
const hideFooter = computed(() => {
  return route.meta.hideFooter === true;
})

const titlePage = usePageTitle()



</script>

<style scoped>
.page-header {
  position: relative;
  height: 3rem;           /* 48px */
  padding: 0 1rem;        /* 16px */
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

.main-container {
  padding-bottom: 4rem;   /* 64px */
}
</style>

