<template>
  <q-page class="q-px-md q-pt-sm q-mt-md">
    <div class="main-container flex column item-center justify-center">

      <!-- Balance -->
      <div class="flex items-center justify-between ">
        <div class="typography-body-md-regular text-black">موجودی شما:</div>
        <div>
          <span class="typography-body-md-regular text-black q-ml-xs">۱۶۵,۵۵۷,۰۰۰</span>
          <span class="typography-caption-md-regular text-grey-custom">ریال</span>
        </div>
      </div>

      <!-- Input for gold amount -->
      <div class="flex column ">
        <div class="flex bg-white-light-active input-div-wrapper">
          <input v-model="goldAmount" type="text" class="input-custom full-width bg-white-light-active" />
          <span class="unit-span">گرم</span>
        </div>
      </div>

      <!-- Price display -->
      <div class="flex column q-mb-xs">
        <div class="flex bg-white-light-active input-div-wrapper q-mb-sm">
          <input v-model="rialAmount" type="text" class="input-custom full-width bg-white-light-active" />
          <span class="unit-span">ریال</span>
        </div>
        <!-- Toman equivalent -->
      <div class="typography-caption-lg-regular text-grey-custom text-right">معادل ۷ میلیون تومان</div>
      </div>



      <!-- Button -->
      <div class="flex flex-center">
        <ButtonComponent label="خرید" size="lg" />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import ButtonComponent from 'src/components/ButtonComponent.vue';
import { ref } from 'vue';

const goldAmount = ref('');
const rialAmount = ref('')
</script>

<style scoped>
.main-container {
  gap: 1.5rem;
  padding: 1.5rem 1rem;
}

.input-div-wrapper {
  padding: 0.625rem 0.5rem;        /* 10px 8px */
  position: relative;
  border-radius: 0.5rem;           /* 8px */
  min-height: 2.75rem;             /* 44px */
  border: 1px solid rgba(217, 217, 217, 0.5);
}

.unit-span {
  position: absolute;
  top: 0.625rem;                   /* 10px */
  left: 0.5rem;                    /* 8px */
  padding-right: 0.5rem;          /* 8px */
  border-right: 1px solid rgba(217, 217, 217, 1);
}

.input-div-wrapper:focus-within {
  background-color: var(--white-light-active);
  border: 1px solid var(--orange-primary);
}

.input-custom {
  border: none;
  outline: none;
  direction: ltr;
  padding-left: 2.5rem;           /* 40px */
  font-size: 1rem;                /* 16px */
}

.input-custom:focus {
  background-color: var(--white-light-active);
}

.price-display {
  background-color: rgba(240, 240, 240, 1);
  padding: 0.75rem 1rem;          /* 12px 16px */
  border-radius: 0.5rem;          /* 8px */
}
</style>

