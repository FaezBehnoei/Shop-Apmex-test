<template>
  <q-page class="q-px-md q-mt-md q-mb-md" >

    <!-- ۱) نوار فیلتر -->
    <nav class="filter-bar">
      <button
        v-for="f in filters"
        :key="f.value"
        :class="['filter-btn typography-caption-md-regular flex flex-center text-grey-normal', { active: selectedFilter === f.value }]"
        @click="selectedFilter = f.value"
      >
        <!-- <SvgIcon
        v-if="f.value === 'all'"
        name="search-bar"
        state="black"
        size="24"
        class="q-ml-xs"
      /> -->
        {{ f.label }}
      </button>
    </nav>
    <!-- search bar  -->
     <div class="flex items-center justify-between q-mb-md">
      <div class="parent-div">
        <div class="q-ml-md">
          <input v-model="searchQuery" type="text" class="custom-searchQuery full-width" placeholder="جستجو"/>
        </div>
        <SvgIcon name="search" state="black" size="24" class="search-icon"/>
      </div>
      <button @click="openFilterDialog = true" class="bg-white-light-active custom-btn-filter flex flex-center">
        <SvgIcon name="filter" state="black" size="24" />
      </button>
     </div>

    <!-- ۲) گروه‌بندی بر اساس تاریخ و رندر تراکنش‌ها -->

    <div v-if="Object.keys(txStore.groupedTransactions).length !== 0">
      <template v-for="(group, date) in txStore.groupedTransactions" :key="date">
      <!-- جداکنندهٔ تاریخ -->
      <div class="date-separator">
        <div class="date-line"></div>
        <div class="date-text">{{ date }}</div>
        <div class="date-line"></div>
      </div>

      <!-- تراکنش‌های همان تاریخ -->
      <div
        v-for="tx in group"
        :key="tx.id"
        class="transaction-item"
      >
        <div class="transaction-content">
          <!-- سمت چپ -->
          <div class="transaction-left">
            <div class="flex items-center">
              <div class="transaction-amount flex items-center q-mb-md">
              <span class="amount-value typography-body-md-regular text-blue-custom">{{ tx.amount }}</span>
              <span class="amount-currency typography-caption-md-regular text-white-dark-hover q-pr-xs">ریال</span>
              <div class="transaction-type typography-body-md-regular text-blue-custom q-mr-sm" :class="tx.typeColor">
              {{ tx.type }}
            </div>
            </div>

            </div>
            <div class="transaction-time typography-caption-md-regular text-white-dark-hover">
              {{ tx.date }}<span class="q-px-xs">-</span>{{ tx.time }}
            </div>
          </div>

          <!-- سمت راست -->
          <div class="transaction-right">
            <div
              class="transaction-status typography-caption-md-regular"
              :class="tx.statusColor"
            >
              {{ tx.statusText }}
            </div>
            <div class="transaction-more">
              <span class="more-text typography-caption-md-regular text-black-custom">بیشتر</span>
              <SvgIcon name="arrow-left" state="black" size="16" />
            </div>
          </div>
        </div>
      </div>
    </template>
    </div>

    <!-- Empty state  -->
     <template v-else>
        <EmptyStatesComponent
          title="هیچ تراکنشی ثبت نشده است !!"
          :showButton="true"
          buttonText="فروشگاه"
          :onClick="() => $router.push('/store')"
        />

     </template>

    <FilterPage v-model:modal-value="openFilterDialog"/>
  </q-page>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import SvgIcon from 'src/components/SvgIcon.vue'
import { useTransactionsStore } from 'src/stores/useTransactionsStore'
import FilterPage from './FilterPage.vue'
import EmptyStatesComponent from 'src/components/EmptyStatesComponent.vue'

const openFilterDialog = ref(false)
const txStore = useTransactionsStore()

const filters = [
  { label: 'نمایش همه', value: 'all' },
  { label: 'واریز',     value: 'واریز' },
  { label: 'برداشت',    value: 'برداشت' },
  { label: 'طلا',       value: 'طلا' },
  { label: 'نقره',      value: 'نقره' },
  { label: 'شمش',       value: 'شمش' }
]

const selectedFilter = ref('all')
const searchQuery = ref('')

// اعمال فیلتر در هر بار تغییر selectedFilter یا searchQuery
watch([selectedFilter, searchQuery], ([cat, search]) => {
  txStore.applyFilters({
    category: cat,
    search: search
  })
})

// بارگذاری اولیه با فیلترهای localStorage (اختیاری)
onMounted(async () => {
  const saved = localStorage.getItem('account-filters')
  if (saved) {
    const parsed = JSON.parse(saved)
    await txStore.applyFilters(parsed)
  } else {
    await txStore.fetchTransactions()
  }
})
console.log(txStore.groupedTransactions)
</script>


<style scoped>
/* -------------------------------- */
/* نوار فیلتر */
.filter-bar {
  display: flex;
  overflow-x: auto;
  gap: 1rem; /* 32px */
  scrollbar-width: none;
  margin-bottom: 1.5rem; /* 24px */
}
.filter-btn {
  flex: 0 0 auto;
  border: 1px solid var(--white-dark);
  min-width: 2.5rem;
  padding: 0.25rem;
  border-radius: 57px;
  cursor: pointer;
  background-color: transparent;
}
.filter-btn.active {
  color: var(--orange-primary);
  background-color: rgba(255, 239, 229, 1);
  border-color: var(--orange-primary);
}
/* -------------------------------- */

/* جداکنندهٔ تاریخ */
.date-separator {
  display: flex;
  align-items: center;
  padding: 0 0 1rem 0; /* 16px 0 */
}
.date-line {
  flex: 1;
  height: 0.0625rem; /* 1px */
  background-color: #e0e0e0;
}
.date-text {
  padding: 0 0.75rem; /* 12px */
  font-size: 0.75rem; /* 12px */
  color: #757575;
}

/* هر تراکنش */
.transaction-item {
  background-color: #ffffff;
  border-radius: 0.5rem; /* 8px */
  margin-bottom: 1rem;   /* 16px */
  box-shadow: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.1); /* 1px 2px */
  overflow: hidden;
}
.transaction-content {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 1rem; /* 8px 16px */
  align-items: center;
  background-color: var(--white-light-active);
}

/* سمت چپ */
.transaction-left {
  display: flex;
  flex-direction: column;
}
.transaction-amount {
  display: flex;
  align-items: baseline;
}

/* سمت راست */
.transaction-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.transaction-status {
  padding: 0.125rem 0.5rem; /* 2px 8px */
  border-radius: 0.25rem;   /* 4px */
  margin-bottom: 1rem;      /* 16px */
}
.transaction-status.success {
  color: var(--q-positive);
}
.transaction-status.failed {
  color: var(--q-negative);
}
.transaction-status.pending {
  color: var(--orange-primary);
}
.transaction-more {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.more-text {
  margin-left: 0.25rem; /* 4px */
}

.parent-div {
  position: relative;
  flex: 1;
  max-width: 100%;
}

.custom-searchQuery {
  height: 2.0625rem;         /* 33px */
  padding: 0 2rem 0 0;     /* 0 40px 0 0 */
  border: none;
  border-radius: 0.5rem;     /* 8px */
  background-color: #F0F0F0;
  font-size: 0.875rem;       /* 14px */
  color: #333;
  outline: none;
  box-sizing: border-box;
}

.search-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: 0.5rem; /* 12px */
}

.custom-btn-filter {
  padding: 0.3rem;
  background-color: var(--white-light-active);
  border-radius: 0.256rem; /* 8px */
  border: none;
  cursor: pointer;
}
.text-orange-primary{
  color: var(--orange-primary);
}
</style>

