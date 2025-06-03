<template>
  <div v-if="modelValue" class="modal-overlay flex items-end justify-center">
    <div class="modal-sheet">
       <!-- Header -->
      <div class="header-icon flex items-center">
        <div @click="$emit('update:modelValue', false)">
          <SvgIcon name="close" state="black" size="24"  class="close-icon" />
        </div>
        <div class="full-width text-center">
          <span class="typography-body-md-medium text-grey-darker">{{ title }}</span>
        </div>
      </div>

      <!-- Info List -->
      <div class="modal-body q-px-md q-pb-xl">
        <div v-for="(item, index) in details" :key="index" class="info-row flex justify-between q-mb-sm">
          <span class="typography-body-md-regular label-color">{{ item.label }}:</span>
          <span class="typography-body-md-regular text-black text-left">{{ item.value }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SvgIcon from 'src/components/SvgIcon.vue'

defineProps({
  modelValue: { type: Boolean, required: true },
  title:      { type: String, required: true },
  details:    {
    type: Array,
    required: true,
    validator: (arr) =>
      arr.every(
        (item) => typeof item.label === 'string' && typeof item.value === 'string'
      )
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
  z-index: 9999;
}

.modal-sheet {
  width: 100%;
  background-color: #FFFFFF;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}

.modal-header {
  border-bottom: 1px solid #E6E6E6;
  min-height: 3rem;
}

.modal-body {
  background-color: #FFFFFF;
  padding-top: 1rem;
}

.info-row {
  min-height: 2.25rem;
  align-items: center;
  border-bottom: 1px solid rgba(242, 242, 242, 1);
}
.header-icon {
  position: relative;
  min-height: 3rem;
  padding: 1rem;
  border-bottom: 1px solid #E6E6E6;
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 0.5rem;
  transform: translateY(-50%);
  cursor: pointer;
}
.label-color{
  color : #8A8A8A;
}
</style>
