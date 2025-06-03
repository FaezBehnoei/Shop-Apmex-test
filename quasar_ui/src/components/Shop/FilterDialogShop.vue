<template>
  <div v-if="modalValue" class="modal-overlay flex items-center justify-center">
    <div class="modal-content">
      <!-- Header -->
      <div class="header-icon flex items-center q-mb-md">
        <SvgIcon name="close" state="black" size="24" @click="$emit('update:modalValue', false)" class="close-icon" />
        <div class="full-width text-center">
          <span class="typography-body-lg-bold text-grey-darker">فیلترها</span>
        </div>
      </div>

      <!-- Dropdown Filters -->
      <div class="filter-section">
        <DropDownFilterComponent v-model="filters.type" :options="typeOptions" placeholder="نوع" class="q-mb-sm" />
        <DropDownFilterComponent v-model="filters.gram" :options="gramOptions" placeholder="گرم" class="q-mb-sm" />
        <PricedropDownComponent v-model:modelValueFrom="priceFrom"
          v-model:modelValueTo="priceTo"
          v-model:modelValueRange="priceRange"
          :min-value="0"
          :max-value="500_000_000"
          :step-value="1000"
          class="q-mb-sm" />
        <DropDownFilterComponent v-model="filters.model" :options="modelOptions" placeholder="مدل" class="q-mb-sm" />
        <DropDownFilterComponent v-model="filters.brand" :options="brandOptions" placeholder="برند" class="q-mb-sm" />
      </div>

      <!-- Action Buttons -->
      <div class="button-row flex justify-between q-mt-lg">
        <ButtonComponent label="حذف فیلتر" type="stroke" size="lg" class="button-clear" @click="clearFilters" />
        <ButtonComponent label="تایید فیلتر" type="primary" size="lg" class="button-apply" @click="applyFilters" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SvgIcon from 'src/components/SvgIcon.vue'
import ButtonComponent from 'src/components/ButtonComponent.vue'
import DropDownFilterComponent from './DropDownFilterComponent.vue'
import PricedropDownComponent from './PricedropDownComponent.vue'

defineProps({
  modalValue: Boolean
})
const priceFrom = ref('')
const priceTo = ref('')
const priceRange = ref([0, 500000000])

const emit = defineEmits(['update:modalValue', 'apply'])

const filters = ref({
  type: '',
  gram: '',
  title: '',
  model: '',
  brand: ''
})

const typeOptions = ['سکه', 'شمش', 'طلای آب‌شده']
const gramOptions = ['1', '2', '5', '10']
const modelOptions = ['کلاسیک', 'مدرن']
const brandOptions = ['گلدیس', 'زرین']

function clearFilters() {
  filters.value = { type: '', gram: '', title: '', model: '', brand: '' }
  emit('apply', filters.value)
  emit('update:modalValue', false)
}

function applyFilters() {
  emit('apply', filters.value)
  emit('update:modalValue', false)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.modal-content {
  background-color: white;
  overflow-y: auto;
  position: fixed;
  flex-direction: column;
  border-radius: 1.25rem 1.25rem 0 0;
  bottom: 0;
  right: 0;
  left: 0;
  padding: 1rem;
  max-height: calc(100vh - 2rem);
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

.button-row {
  gap: 1rem;
}

.button-clear {
  flex: 1;
}

.button-apply {
  flex: 1;
}
</style>
