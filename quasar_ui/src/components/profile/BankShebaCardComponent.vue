<template>
  <div class="sheba-card row items-center justify-between">
    <!-- لوگوی بانک -->
    <div class="flex justify-between items-center full-width">
      <div class="flex items-center">
        <img :src="bankLogo" alt="bank-logo" class="bank-logo" />
        <div class="typography-body-md-medium text-white-darker q-mr-xs">
          {{ bankName }}
        </div>
      </div>
      <div>
        <SvgIcon name="shetab-profile" state="colored" size="24"/>
      </div>
    </div>

    <div class="devider q-my-sm"></div>

    <!-- شماره شبا -->
    <div class="full-width text-center q-mt-sm">
      <span class="typography-subtitle-bold text-black sheba-text">
        {{ sheba }}
      </span>
    </div>
  </div>
</template>

<script setup>
import SvgIcon from '../SvgIcon.vue';
defineProps({
  sheba: { type: String, required: true },
  bankName: { type: String, required: true },
  bankLogo: { type: String, required: true }
})
</script>

<style scoped>
.sheba-card {
  background-color: #f8f8f8;
  border: 1px solid #dfe1e5;
  border-radius: 8px;
  padding: 1rem;
  flex-direction: column;
}

.bank-logo {
  width: 24px;
  height: 24px;
}

.sheba-text {
  direction: ltr;
  unicode-bidi: plaintext;
  font-family: monospace, 'IRANYekanWeb';
}
.devider{
  width: 100%;
  height: 0.35rem;
  background: linear-gradient(to left,#DAE7EE , #F6FCFF)
}
</style>
