<template>
  <q-page>
    <!-- title  -->
     <div class="flex justify-between items-center title-div">
      <span class="typography-body-md-bold text-blue-custom">کیف پول گلدیس</span>
      <div class="percents-div flex column">
        <span class="inside-title">سود و زیان (تومان)</span>
        <div class="flex">
          <span class="typography-caption-md-regular text-black q-ml-sm">۱۶,۵۵۷,۰۰۰</span>
          <span :class="profit >= 0 ? 'text-positive' : 'text-negative'" class="typography-caption-md-regular">
            {{ profit }}%{{ profit >= 0 ? '+' : '' }}
          </span>
        </div>
      </div>
     </div>
     <!-- navbar  -->
      <div>
        <ul class="flex items-center justify-evenly ul-style-wallet">
          <li  @click="handleTabClick(item.title)" :class="active === item.title ? 'activated-list' : ''" class="q-px-md flex flex-center text-white-darker list-items" v-for="item in navList" :key="item.id">{{ item.title }}</li>
        </ul>
      </div>
      <!-- pages  -->
        <!-- DonatChart  -->
          <div v-if="active === 'دارایی ها'" class="donatChart-div ">
            <DonatChartComponent />
          </div>
        <!-- History page  -->
         <div v-if="active === 'گردش حساب' ">
          <HistoryPage />
         </div>
         <!-- shop avilable page -->
        <div v-if="active === 'موجودی شمش' ">
            <ShopCards  class="q-mb-md"/>
         </div>
  </q-page>
</template>
<script setup>
import DonatChartComponent from 'src/components/DonatChartComponent.vue';
import { ref, onMounted } from 'vue';
import HistoryPage from './HistoryTransactions/HistoryPage.vue';
import ShopCards from './ProductsShop/ShopCards.vue';

const profit = ref(16.23)
const navList = ref([
  {id:1, title:'دارایی ها',route:''},
  {id:2, title:'موجودی شمش',route:''},
  {id:3, title:'گردش حساب',route:''},
])

const active = ref('دارایی ها')

function handleTabClick(title) {
  active.value = title
  localStorage.setItem('wallet-tab', title)
}


onMounted(() => {
  const savedTab = localStorage.getItem('wallet-tab')
  if (savedTab) {
    active.value = savedTab
    localStorage.removeItem('wallet-tab')
  }
})


</script>

<style scoped>
.title-div {
  padding: 1rem 1rem 0.5rem 1rem;
}

.percents-div {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  background-color: var(--white-light-active);
  cursor: pointer;
}

.percents-div:hover {
  background-color: var(--white-light-hover);
}

.inside-title {
  font-weight: 400;
  font-size: 0.5rem;       /* 8px */
  line-height: 0.875rem;   /* 14px */
  letter-spacing: 0%;
  color: var(--white-dark);
}

.inside-title:active {
  color: var(--white-dark-active);
}

.ul-style-wallet {
  border-bottom: 0.125rem solid var(--white-light-active); /* 2px */
}

.ul-style-wallet > li {
  position: relative;
  padding: 0.625rem; /* 10px */
  min-width: 7.1456rem; /* 114.33px */
}
.list-items{
  font-weight: 400;
  font-size: 0.75rem;
  line-height: 1.125rem;
  letter-spacing: 0%;
}
.activated-list {
  font-weight: 700;
  color: rgba(102, 191, 161, 1);
}

.activated-list::after {
  content: "";
  position: absolute;
  bottom: -0.125rem;  /* -2px */
  right: 0;
  left: 0;
  height: 0.125rem;   /* 2px */
  background-color: rgba(102, 191, 161, 1);
}

.flex-grow-1 {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.donatChart-div {
  padding: 2rem 0.96875rem 1rem 0.96875rem; /* 32px 15.5px 16px 15.5px */
}
</style>

