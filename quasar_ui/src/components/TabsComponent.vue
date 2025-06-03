<template>
  <div class="tab-bar-wrapper full-width">
    <div class="tab-bar  q-mx-auto" ref="tabScroll">
      <div
        v-for="(tab, index) in tabs"
        :key="`${tab}-${index}`"
        :class="['tab-items' , {active : activeTab === index}]"
        class="typography-caption-lg-regular text-white-darker q-mx-auto flex flex-center"
        @click="activeTab = index"
      >
      {{ tab }}
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref,watch } from 'vue';

const tabs = ref(['بررسی بازار', 'نمودار طلا', 'نمودار نقره', 'نمودار دلار'])
const activeTab = ref(1)
const tabScroll = ref('')

watch(activeTab, () => {
  const tabsEl = tabScroll.value?.children
  if (tabsEl && tabsEl[activeTab.value]) {
    tabsEl[activeTab.value].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
  }
})
</script>

<style scoped>
.tab-bar-wrapper {
  padding-inline: 1rem; /* 16px */
  width: 100%;
  border-bottom: 0.125rem solid rgba(241, 241, 241, 1); /* 2px */
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.tab-bar-wrapper::-webkit-scrollbar {
  display: none;
}

.tab-bar {
  display: flex;
}

.tab-items {
  padding: 0.625rem; /* 10px */
  min-width: 6.17rem; /* 98.75px */
}

.tab-items.active {
  color: rgba(102, 191, 161, 1);
  border-bottom: 0.125rem solid rgba(102, 191, 161, 1); /* 2px */
}
</style>

