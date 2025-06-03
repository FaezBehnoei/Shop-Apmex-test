<template>
  <div class="empty-state-container column items-center justify-center q-px-xl q-mt-xl q-pb-md">
    <!-- Icon -->
    <div>
      <SvgIcon :name="icon" :state="state" :size="size" class="empty-state-icon q-mb-md"/>
    </div>

    <!-- Title -->
    <div class="empty-state-title typography-body-md-bold text-center text-black q-mb-sm q-pb-sm">
      {{ title }}
    </div>

    <!-- Subtitle -->
    <div
      v-if="subtitle"
      class="empty-state-subtitle typography-caption-md-regular text-center text-grey q-mb-md "
    >
      {{ subtitle }}
    </div>

    <div class="q-px-xl q-mt-sm full-width">
      <!-- Button -->
    <ButtonComponent
      v-if="showButton"
      :label="buttonText"
      color="primary"
      type="stroke"
      size="lg"
      class="full-width"
      @click="onClick"
    />
    </div>
  </div>
</template>

<script setup>
import ButtonComponent from './ButtonComponent.vue';
import SvgIcon from './SvgIcon.vue';

defineProps({
  icon: { type: String, default: 'empty-history-factor' },
  state: { type: String, default: 'colored' },
  size: { type: String, default: '24' },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  showButton: { type: Boolean, default: false },
  buttonText: { type: String, default: 'بازگشت' },
  onClick: { type: Function, default: () => {} },
})
</script>

<style scoped lang="scss">
.empty-state-container {
  min-height: 40vh;
  text-align: center;
}

.empty-state-icon {
  width: 7.625rem !important;
  object-fit: contain;
}



.empty-state-subtitle {
  color: #999;
  line-height: 1.5;
  max-width: 280px;
  margin: 0 auto;
}

</style>
