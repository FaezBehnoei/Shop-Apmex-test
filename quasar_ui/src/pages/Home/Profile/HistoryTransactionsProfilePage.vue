<template>
  <q-page class="q-px-md q-mt-md q-mb-md">

    <!-- نوار فیلتر -->
    <nav class="filter-bar q-mb-md">
      <button
        v-for="f in filters"
        :key="f.value"
        :class="['filter-btn typography-caption-md-regular flex flex-center text-grey-normal', { active: selectedFilter === f.value }]"
        @click="selectedFilter = f.value"
      >
        {{ f.label }}
      </button>
    </nav>

    <!-- جستجو -->
    <div class="flex items-center justify-between">
      <div class="parent-div"  :class="{ 'focused-parent': isFocused }">
        <div>
          <input v-model="searchQuery" type="text" class="custom-searchQuery full-width" placeholder="جستجو"/>
        </div>
        <SvgIcon name="search" state="black" size="24" class="search-icon" />
      </div>
    </div>

    <!-- لیست گروه‌بندی‌شده -->
    <template v-for="(group, date) in groupedTransactions" :key="date">
      <div class="date-separator">
        <div class="date-line"></div>
        <div class="date-text">{{ date }}</div>
        <div class="date-line"></div>
      </div>

      <div v-for="tx in group" :key="tx.id" class="transaction-item">
        <div class="transaction-content">
          <!-- سمت چپ -->
          <div class="transaction-left">
            <div class="transaction-type typography-caption-md-regular text-blue-custom q-mb-xs">
              {{ tx.title }}
            </div>
            <div class="transaction-amount typography-body-md-regular text-blue-custom">
              <!-- اگر description داشت، نمایش بده؛ وگرنه amount -->
              <template v-if="tx.description">
                {{ tx.description }}
              </template>
              <template v-else>
                {{ tx.amount.toLocaleString() }}
                <span class="typography-caption-md-regular text-white-dark-hover q-pr-xs">ریال</span>
              </template>
            </div>
            <div class="transaction-time typography-caption-md-regular text-white-dark-hover q-mt-xs">
              {{ tx.date }} - {{ tx.time }}
            </div>
          </div>

          <!-- سمت راست -->
          <div class="transaction-right items-start">
            <div class="transaction-status full-width typography-caption-md-regular text-right" :class="statusColorClass(tx.status)">
              {{ statusText(tx.status) }}
            </div>
            <div @click="openDialog(tx)" class="transaction-more flex items-center q-mt-sm">
              <span class="more-text typography-caption-md-regular text-black-custom">بیشتر</span>
              <SvgIcon name="arrow-back-l" state="black" size="16" class="q-ml-xs" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <DialogHistoryProfile
      v-model="showModal"
      :title="selectedDialogTitle"
      :details="selectedDialogDetails"
    />
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import SvgIcon from 'src/components/SvgIcon.vue';
import { getProfileTransactions } from 'src/services/profileServices';
import DialogHistoryProfile from 'src/components/profile/DialogHistoryProfile.vue';

const isFocused = ref(false)
const showModal = ref(false)

const filters = [
  { label: 'نمایش همه', value: 'all' },
  { label: 'واریز',     value: 'واریز' },
  { label: 'برداشت',    value: 'برداشت' },
  { label: 'طلا',       value: 'طلا' },
  { label: 'نقره',      value: 'نقره' },
  { label: 'شمش',       value: 'شمش' }
];

const selectedFilter = ref('all');
const searchQuery = ref('');
const selectedDialogDetails = ref('')
const selectedDialogTitle = ref('')


const allTransactions = ref([]);

function openDialog(tx){
  selectedDialogDetails.value = tx.details || ''
  selectedDialogTitle.value = tx.dialog_title || ''
  showModal.value = true
}

const groupedTransactions = computed(() => {
  return allTransactions.value.reduce((acc, tx) => {
    if (!acc[tx.date]) acc[tx.date] = [];
    acc[tx.date].push(tx);
    return acc;
  }, {});
});

function statusColorClass(status) {
  return {
    3: 'text-positive',
    1: 'text-negative',
    2: 'text-orange-primary'
  }[status] || '';
}

function statusText(status) {
  return {
    3: 'موفق',
    1: 'ناموفق',
    2: 'درحال انجام'
  }[status] || '';
}

watch([selectedFilter, searchQuery], async([cat, search]) => {
  const filter = {
    category: cat,
    search: search
  }
  const data = await getProfileTransactions(filter)
  allTransactions.value = Object.values(data).flat()
})

onMounted(async() => {
 const data = await getProfileTransactions()
 allTransactions.value = Object.values(data).flat()
})
</script>
<style scoped>
.filter-bar {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  scrollbar-width: none;
}
.filter-btn {
  flex: 0 0 auto;
  border: none;
  cursor: pointer;
  background-color: transparent;
  padding: 0.35rem;
  border: 1px solid var(--white-dark);
  border-radius: 57px;
}
.filter-btn.active {
  background-color: #FFEFE5;
  color: var(--orange-primary);
  border: 1px solid var(--orange-primary);
}
.parent-div {
  position: relative;
  flex: 1;
  max-width: 100%;
}
.custom-searchQuery {
  width: 100%;
  height: 2.0625rem;         /* 33px */
  padding: 0 2rem 0 0;     /* 0 40px 0 0 */
  border: none;
  border-radius: 0.5rem;     /* 8px */
  background-color: #F0F0F0;
  font-size: 0.875rem;       /* 14px */
  color: #333;
  outline: none;
}
.focused-parent {
  border: 1px solid var(--orange-primary);
  border-radius: 8px;
  background-color: white;
  transition: all 0.2s ease;
}

.search-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
}
.date-separator {
  display: flex;
  align-items: center;
  padding: 1rem 0;
}
.date-line {
  flex: 1;
  height: 1px;
  background-color: #e0e0e0;
}
.date-text {
  padding: 0 0.75rem;
  font-size: 0.75rem;
  color: #757575;
}
.transaction-item {
  background-color: #fff;
  border-radius: 8px;
  margin-bottom: 1rem;
  overflow: hidden;
}
.transaction-content {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 1rem;
  background-color: var(--white-light-active);
}
.transaction-left {
  display: flex;
  flex-direction: column;
}
.transaction-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.transaction-status {
  border-radius: 4px;
  margin-bottom: 0.75rem;
}
.transaction-more {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.more-text {
  margin-left: 0.25rem;
}
</style>
