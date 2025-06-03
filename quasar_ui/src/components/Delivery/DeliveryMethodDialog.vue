<template>
  <div v-if="modalValue" class="modal-overlay flex row items-center">
    <div class="modal-content full-width">
      <!-- header  -->
      <div class="header-icon flex items-center q-mb-md">
        <SvgIcon name="close" state="black" size="24" @click="$emit('update:modalValue', false)" class="close-icon"/>
        <div class="full-width text-center">
          <span class="typography-body-md-medium text-grey-darker">روش دریافت</span>
        </div>
      </div>

      <div class="q-px-md">
        <!-- Selection options -->
        <div class="delivery-question q-mb-sm">
          <span class="typography-body-md-medium text-black">کالای خود را از چه طریقی میخواهید دریافت کنید؟</span>
        </div>

        <div class="delivery-options">
          <!-- In-person delivery option -->
          <div class="delivery-option flex items-center q-mb-sm">
            <div class="radio-wrapper flex items-center justify-center" @click="selectedOption = 'inPerson'">
              <div class="radio-circle" :class="{ 'radio-selected': selectedOption === 'inPerson' }">
                <div v-if="selectedOption === 'inPerson'" class="radio-inner"></div>
              </div>
            </div>
            <div class="option-text flex-grow">
              <span class="typography-body-md-medium text-black">تحویل حضوری</span>
              <span class="typography-caption-md-regular text-grey-dark d-block">(تحویل از فروشگاه های گلدیس)</span>
            </div>
          </div>

          <!-- Post delivery option -->
          <div class="delivery-option flex items-center q-mb-md">
            <div class="radio-wrapper flex items-center justify-center" @click="selectedOption = 'byPost'">
              <div class="radio-circle" :class="{ 'radio-selected': selectedOption === 'byPost' }">
                <div v-if="selectedOption === 'byPost'" class="radio-inner"></div>
              </div>
            </div>
            <div class="option-text flex-grow">
              <span class="typography-body-md-medium text-black">ارسال با پیک</span>
              <span class="typography-caption-md-regular text-grey-dark d-block">(ارسال کالاهای زیر یک گرم توسط پیک انجام میشود)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Confirm button -->
      <div class="q-px-md">
        <ButtonComponent @click="handleRoutes" size="lg" label="تایید" type="primary" class="custom-btn-confirm full-width" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SvgIcon from 'components/SvgIcon.vue';
import ButtonComponent from 'components/ButtonComponent.vue';
import { useRouter } from 'vue-router';

const router = useRouter()
defineProps({
  modalValue: { type: Boolean, required: true },
});

defineEmits(['update:modalValue']);

const selectedOption = ref('inPerson');

function handleRoutes() {
  if (selectedOption.value === 'inPerson') {
    router.push({ path: '/account/delivery-inperson', query: { method: 'inPerson' } });
  } else {
    router.push({ path: '/account/delivery-inperson', query: { method: 'byPost' } });
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
  background-color: rgba(244, 244, 244, 1);
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
}

.header-icon {
  position: relative;
  min-height: 3rem;
  padding: 0.5rem 1rem;
  border-bottom: 0.0625rem solid rgba(230, 230, 230, 1);
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 0.5rem;
  transform: translateY(-50%);
  cursor: pointer;
}

.delivery-question {
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
}

.delivery-option {
  padding: 0.5rem 0;
}

.radio-wrapper {
  margin-left: 1rem;
}

.radio-circle {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  border: 0.125rem solid #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.radio-selected {
  border-color: #FF7F33;
}

.radio-inner {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background-color: #FF7F33;
}

.option-text {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.custom-btn-confirm {
  background-color: #FF7F33;
  font-weight: 700;
  font-size: 0.875rem;
  line-height: 1.125rem;
  border-radius: 0.5rem;
  margin-bottom: 2.25rem;
  margin-top: 4rem;
  text-align: center;
  cursor: pointer;
  border: none;
}
</style>

