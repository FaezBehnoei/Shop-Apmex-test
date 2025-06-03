<template>
  <div v-if="modalValue" class="modal-overlay flex row items-center justify-center">
    <div class="modal-content full-width">
      <!-- Header -->
      <div class="header-icon flex items-center q-mb-md">
        <div @click="$emit('update:modalValue', false)">
          <SvgIcon name="close" state="black" size="24"  class="close-icon" />
        </div>
        <div class="full-width text-center">
          <span class="typography-body-md-medium text-grey-darker">{{ title }}</span>
        </div>
      </div>

      <div class="q-px-md">
        <!-- Time -->
        <p class="typography-caption-md-regular text-grey-dark q-mb-sm">{{ timestamp }}</p>
        <!-- Message -->
        <p class="typography-body-md-regular text-black">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import SvgIcon from 'components/SvgIcon.vue';

 defineProps({
  modalValue: { type: Boolean, required: true },
  title: { type: String, required: true },
  message: { type: String, required: true },
  timestamp: { type: String, required: true }
})

defineEmits(['update:modalValue'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(0.125rem);
  -webkit-backdrop-filter: blur(0.125rem);
  z-index: 9999;
}

.modal-content {
  background-color: #fff;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
  padding-bottom: 4rem;
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
</style>
