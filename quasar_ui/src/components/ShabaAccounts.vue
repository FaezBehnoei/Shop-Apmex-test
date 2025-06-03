<template>
  <div class="account-card">
    <div
      v-for="account in accounts"
      :key="account.id"
      class="account-item flex items-center justify-between"
      @click="selectAccount(account.number)"
    >
      <!-- right side -->
      <div class="flex items-center">
        <div class="radio-wrapper flex flex-center">
          <div v-if="modelValue === account.number" class="radio-dot"></div>
        </div>
        <div :class="['typography-body-md-medium', modelValue === account.number ? 'text-orange-primary' : 'text-blue-custom']">
          {{ account.number }}
        </div>
      </div>

      <SvgIcon name="dots" state="black" size="24" class="q-ml-xs" />
    </div>

    <div class="add-account flex items-center q-mt-md">
      <SvgIcon name="plus" state="black" size="24" class="q-ml-xs" />
      <span class="typography-caption-lg-regular text-blue-custom">شماره حساب جدید</span>
    </div>
  </div>
</template>

<script setup>
import SvgIcon from 'src/components/SvgIcon.vue'
import { computed } from 'vue'

const props = defineProps({
  modelValue: String // شماره شبا انتخاب‌شده
})

const emit = defineEmits(['update:modelValue'])

const accounts = [
  { id: 1, number: 'IR120700004567890001234567' },
  { id: 2, number: 'IR230800004567890001234567' },
  { id: 3, number: 'IR340900004567890001234567' }
]

const selected = computed({
  get: () => props.modelValue,
  set: val => emit('update:modelValue', val)
})

function selectAccount(shaba) {
  selected.value = shaba
}
</script>


<style scoped>
.account-card {
  background-color: var(--white-light-active);
  border-radius: 0.5rem;
  padding: 0.5rem 1rem 2rem 1rem;
}
.account-item {
  padding: 0.5rem 0;
  cursor: pointer;
  min-height: 2.375rem;
  margin-bottom: 0.5rem;
}
.radio-wrapper {
  width: 0.625rem;
  height: 0.625rem;
  border: 1px solid var(--white-darker);
  border-radius: 50%;
  margin-left: 0.5rem;
}
.radio-dot {
  padding: 0.2rem;
  background-color: rgba(255, 127, 51, 1);
  border-radius: 50%;
}
.add-account {
  cursor: pointer;
}
</style>
