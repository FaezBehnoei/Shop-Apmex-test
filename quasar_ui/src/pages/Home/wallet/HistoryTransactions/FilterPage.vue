<!-- FilterPage.vue -->
<template>
  <q-page v-if="modalValue" class="q-px-md filter-page">
    <!-- header -->
      <div class="header-icon flex items-center q-mb-md">
        <SvgIcon name="close" state="black" size="24" @click="$emit('update:modalValue', false)" class="close-icon"/>
        <div class="full-width text-center">
          <span class="typography-body-lg-bold text-grey-darker">جزئیات تحویل</span>
        </div>
      </div>
    <div class="flex column full-height">

      <!-- Date Range -->
      <div class="q-mb-md">
        <div class="typography-body-sm-regular text-dark q-mb-xs">تاریخ</div>
        <div class="flex full-width">
          <div class="filter-input-wrapper q-ml-sm">
            <input v-model="dateFrom" type="text" class="filter-input typography-caption-md-regular full-width" placeholder="از" readonly @click="openDatePickerFrom = true" />
            <q-icon name="event" class="date-icon cursor-pointer" @click="openDatePickerFrom = true" />

            <q-dialog v-model="openDatePickerFrom">
              <q-date
                v-model="dateFrom"
                calendar="persian"
                mask="YYYY/MM/DD"
                today-btn
                @update:model-value="openDatePickerFrom = false"
              />
            </q-dialog>
          </div>

          <div class="filter-input-wrapper">
            <input v-model="dateTo" type="text" class="filter-input typography-caption-md-regular full-width" placeholder="تا" readonly @click="openDatePickerTo = true" />
            <q-icon name="event" class="date-icon cursor-pointer" @click="openDatePickerTo = true" />

            <q-dialog v-model="openDatePickerTo">
              <q-date
                v-model="dateTo"
                calendar="persian"
                mask="YYYY/MM/DD"
                today-btn
                @update:model-value="openDatePickerTo = false"
              />
            </q-dialog>
          </div>
        </div>
      </div>

      <!-- Transaction Status Using DropdownComponent -->
      <div class="q-mb-md">
        <div class="typography-body-sm-regular text-dark q-mb-sm">وضعیت تراکنش</div>
        <DropdownComponent
          v-model="status"
          :options="stateOptions"
          placeholder="همه"
        />
      </div>

      <!-- Transaction Type Using DropdownComponent -->
      <div class="q-mb-md">
        <div class="typography-body-sm-regular text-dark q-mb-sm">نوع تراکنش</div>
        <DropdownComponent
          v-model="type"
          :options="typeOptions"
          placeholder="همه"
        />
      </div>

      <!-- Amount Range -->
      <div class="custom-margin">
        <div class="typography-body-sm-regular text-dark q-mb-sm">مبلغ</div>
        <div class="flex full-width">
          <div class="filter-input-wrapper q-ml-sm">
            <input v-model="amountFrom" type="text" class="filter-input typography-caption-md-regular full-width" placeholder="از" />
          </div>
          <div class="filter-input-wrapper">
            <input v-model="amountTo" type="text" class="filter-input typography-caption-md-regular full-width" placeholder="تا" />
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="flex flex-center">
        <ButtonComponent
          @click="applyFilter" size="xs" label="اعمال فیلتر" type="primary"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ButtonComponent from 'src/components/ButtonComponent.vue'
import DropdownComponent from 'src/components/DropDownComponent.vue'
import { useTransactionsStore } from 'src/stores/useTransactionsStore'
import SvgIcon from 'src/components/SvgIcon.vue'

const router = useRouter()
const store = useTransactionsStore()
defineProps({
  modalValue: { type: Boolean, required: true },
})

const dateFrom = ref('')
const dateTo = ref('')
const status = ref('')
const type = ref('')
const amountFrom = ref('')
const amountTo = ref('')
const emit = defineEmits(['update:modalValue'])


const openDatePickerFrom = ref(false)
const openDatePickerTo = ref(false)

const typeOptions = ['واریز', 'برداشت', 'تبدیل']
const stateOptions = ['همه', 'موفق', 'ناموفق', 'درحال انجام', 'نامشخص']

// اگر بخوای فیلترهای قبلی رو بارگذاری کنی
// onMounted(() => {
//   const saved = localStorage.getItem('account-filters')
//   if (saved) {
//     try {
//       const filters = JSON.parse(saved)
//       dateFrom.value = filters.dateFrom || ''
//       dateTo.value = filters.dateTo || ''
//       status.value = filters.status || ''
//       type.value = filters.type || ''
//       amountFrom.value = filters.amountFrom || ''
//       amountTo.value = filters.amountTo || ''
//     } catch (e) {
//       console.error('خطا در بازیابی فیلترهای ذخیره‌شده:', e)
//     }
//   }
// })

// کلیک روی دکمهٔ "اعمال فیلتر"
function applyFilter() {
  const filters = {
    dateFrom: dateFrom.value,
    dateTo: dateTo.value,
    status: status.value || 'همه',
    type: type.value || 'همه',
    amountFrom: amountFrom.value,
    amountTo: amountTo.value,
  }

  // ذخیره اختیاری در localStorage برای استفاده در onMounted صفحه wallet
  // localStorage.setItem('account-filters', JSON.stringify(filters))

  // اعمال فیلتر روی استور
  store.applyFilters(filters)


  // برگشت به صفحه کیف پول
  router.push('/account/wallet')
  emit('update:modalValue', false)
}
</script>


<style scoped>
.filter-page{
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  background-color: white;
  width: 100%;
  min-height: calc(100vh - 4rem);
}
.filter-input-wrapper {
  flex: 1;
  background-color: var(--white-light-active, #F8F8F8);
  padding: 0.625rem 0.75rem; /* معادل 10px 12px */
  border-radius: 0.5rem; /* 8px */
  min-height: 2.5rem; /* 40px */
  gap: 0.5rem; /* 8px */
  position: relative;
}

.filter-input {
  border: none;
  outline: none;
  background-color: transparent;
  width: calc(100% - 1.5rem);
  color: rgba(130, 130, 130, 1);
}

.date-icon {
  position: absolute;
  left: 0.75rem; /* 12px */
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.page-header {
  position: relative;
  height: 3rem; /* 48px */
  padding: 0 1rem;
  margin-bottom: 1.5rem;
}

.page-header .back-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
}

.custom-margin {
  margin-bottom: 4rem;
}

.header-icon {
  position: relative;
  height: 3.5rem;
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 0rem;
  transform: translateY(-50%);
  cursor: pointer;
}

</style>
