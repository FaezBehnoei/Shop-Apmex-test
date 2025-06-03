<template>
  <div v-if="modalValue" class="modal-overlay flex row items-center">
    <div class="modal-content full-width">
      <!-- header  -->
      <div class="header-icon flex items-center q-mb-md">
        <SvgIcon name="close" state="black" size="24" @click="$emit('update:modalValue', false)" class="close-icon"/>
        <div class="full-width text-center">
          <span class="typography-body-md-medium text-grey-darker">تایید نهایی</span>
        </div>
      </div>

      <div class=" q-px-md">
        <!-- boxes -->
      <div class="info-boxes bg-white">
        <div class="info-row flex justify-between items-center q-mb-sm">
          <span class="typography-body-md-regular text-black">مبلغ برداشت:</span>
          <span class="typography-body-md-regular text-blue-custom">{{ rialBalance }} <span class="typography-caption-md-regular text-blue-custom">تومان</span></span>
        </div>
        <div class="dashed-line q-mb-sm" />
        <div class="info-row flex justify-between items-center q-mb-sm">
          <span class="typography-body-md-regular text-grey-darker">واریز به حساب:</span>
          <span class="typography-body-md-regular text-blue-custom">{{ shebaNumber }}</span>
        </div>
        <div class="dashed-line q-mb-sm" />
        <div class="info-row flex justify-between items-center q-mb-xs">
          <span class="typography-body-md-regular text-grey-darker">موجودی دارایی ریالی:</span>
          <span class="typography-body-md-regular text-blue-custom">  675,7656,768 <span class="typography-caption-md-regular text-blue-custom">تومان</span></span>
        </div>
      </div>


      </div>
      <!-- button -->
      <div class="q-mb-md q-px-md">
        <ButtonComponent @click="confirmWithdraw"  size="lg" label="تایید نهایی" type="primary" class="custom-btn-withdraw full-width" />

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SvgIcon from './SvgIcon.vue';
import ButtonComponent from './ButtonComponent.vue';
import { submitWithdrawRequest } from 'src/services/walletServis'
import { useQuasar } from 'quasar'

const props = defineProps({
  modalValue: { type: Boolean, required: true },
  shebaNumber : String,
  rialBalance : Number,
  assetSlug: String
})
const emit = defineEmits(['update:modalValue'])

const chashAsset = ref('5345453')


const $q = useQuasar()

async function confirmWithdraw() {
  try {
    const payload = {
      asset_slug: props.assetSlug,
      amount: props.rialBalance.replace(/,/g, ''),
      shaba_number: props.shebaNumber,
      chash_amount : chashAsset.value
    }

    await submitWithdrawRequest(payload)

    $q.notify({
      type: 'positive',
      message: 'برداشت با موفقیت ثبت شد.'
    })

    emit('update:modalValue', false)
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'خطا در ثبت برداشت. دوباره تلاش کنید.',
      position: 'top'

    })
    console.error('Withdraw failed:', error)
  }
}


</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  z-index: 9999;
}

.modal-content {
  background-color: rgba(244, 244, 244, 1);
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  padding-bottom: 3.5625rem; /* 57px */
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
}

.header-icon {
  position: relative;
  min-height: 2.5rem; /* 40px */
  padding: 0.5rem 1rem;
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 0.5rem;
  transform: translateY(-50%);
  cursor: pointer;
}

.info-boxes {
  padding: 1rem;
  border-radius: 0.5rem; /* 8px */
  margin-bottom: 2rem; /* 32px */
}

.info-row {
  padding: 0.5rem 0; /* 8px 0 */
}

.dashed-line {
  border-bottom: 1px dashed #ccc;
}

.confirm-btn {
  background: #FF7F33;
  color: white;
  font-weight: bold;
  padding: 0.75rem; /* 12px */
  border-radius: 0.5rem; /* 8px */
  width: 90%;
  max-width: 20rem;
  font-size: 0.875rem; /* 14px */
  border: none;
  cursor: pointer;
}
.confirm-btn:active {
  opacity: 0.8;
}

.custom-btn-withdraw {
  font-weight: 700;
  font-size: 0.75rem; /* 12px */
  line-height: 1.125rem; /* 18px */
  letter-spacing: 0;
  max-width: 100%;
}
</style>

