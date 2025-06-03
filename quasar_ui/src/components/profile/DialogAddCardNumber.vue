<template>
  <div v-if="modelValue" class="modal-overlay flex row items-center justify-center">
    <div class="modal-content full-width">
      <!-- Header -->
      <div class="header-icon flex items-center q-mb-md">
        <div @click="$emit('update:modelValue', false)">
          <SvgIcon name="close" state="black" size="24" class="close-icon" />
        </div>
        <div class="full-width text-center">
          <span class="typography-body-md-medium text-grey-darker">
            {{ title }}
          </span>
        </div>
      </div>

      <!-- Form -->
      <div class="q-px-md">
        <label class="typography-body-md-regular text-black q-mb-xs label-block">
          شماره شبا
        </label>
        <InputComponent
          v-model="sheba"
          placeholder="شماره شبا خود را وارد کنید"
          class="custom-sheba-input q-mb-lg"
        />

        <div>
          <ButtonComponent
          label="تایید"
          color="orange"
          class="full-width"
          @click="handlePostCardNumber"
          :loading="loading"
        />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SvgIcon from 'components/SvgIcon.vue'
import InputComponent from 'components/InputComponent.vue'
import ButtonComponent from 'components/ButtonComponent.vue'
import { postProfileSHebaBankCard } from 'src/services/profileServices'

const props = defineProps({
  modelValue: { type: Boolean, required: true },
  title: { type: String, default: 'تعریف شماره شبا جدید' },
})
const loading = ref(false)

const emit = defineEmits(['update:modelValue', 'submit'])

const sheba = ref('')

// اگر بخوای هنگام باز شدن، مقدار قبلی پاک بشه
watch(() => props.modelValue, (val) => {
  if (val) sheba.value = ''
})

async function handlePostCardNumber(){
  if(loading.value) return;
  loading.value = true
  try{
    await postProfileSHebaBankCard(sheba.value)
    emit('update:modelValue', false)
    emit('submit')
  }finally{
    loading.value = false
  }
}

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
  padding-bottom: 2rem;
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

.label-block {
  display: block;
}

.custom-sheba-input {
  background-color: #f0f0f0;
  border-radius: 8px;
}
</style>
