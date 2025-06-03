<template>
  <div class="main-container q-pa-md q-mx-auto">
    <form @submit.prevent="handleSubmit" class="full-height flex column">

      <!-- back button + logo + title -->
      <div class="flex column items-center">
        <div class="flex items-start full-width q-mb-md">
          <SvgIcon name="arrow-left" state="black" size="24" class="custom-icon" @click="router.go(-1)" cursor="true" />
        </div>
        <img src="../../assets/monograms/Property 1=monogram_color 2_48px.svg" alt="monogram" width="42" class="q-mb-md" />
        <p class="typography-h4-bold text-blue-custom q-mb-md q-mt-sm q-pb-sm">رمز عبور جدید</p>

        <!-- input -->
        <div class="full-width q-mt-md q-px-sm">
          <p class="typography-body-md-regular q-mb-md text-blue-custom text-right">
            رمز عبور جدید خود را وارد کنید
          </p>
          <InputComponent
            label="رمز عبور جدید"
            placeholder="رمز عبور جدید را وارد کنید"
            class="typography-caption-lg-regular"
            v-model="password"
            :type="type"
            :icon="icon"
            state="black"
            Iconsize="16"
            @clicked-icon="handleIcons"
            :highlight="!!password"
            autoInput="true"
          />
        </div>
      </div>

      <!-- confirm button -->
      <div class="flex column items-center custom-margin q-px-sm">
        <ButtonComponent
          :loading="loading"
          size="lg"
          html-type="submit"
          label="تایید"
          type="primary"
          :disable="!password"
          :class="[
            'full-width',
            'margin-input',
            password ? 'bg-orange-primary text-blue-custom ' : 'bg-grey-4 text-blue-custom'
          ]"
        />
      </div>

    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

import ButtonComponent from 'src/components/ButtonComponent.vue';
import InputComponent from 'src/components/InputComponent.vue';
import SvgIcon from 'src/components/SvgIcon.vue';
import { resetPassword } from 'src/services/authService';
import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()
const router = useRouter()
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const otptoken = ref(authStore.otpToken || sessionStorage.getItem('otp_token'))


const type = computed(() => (showPassword.value ? 'text' : 'password'))
const icon = computed(() => (showPassword.value ? 'close-eye' : 'eye'))

async function handleSubmit() {
  if (!password.value) return;
  if(loading.value) return;
  loading.value = true
  try{
    await resetPassword({newPassword: password.value, otpToken: otptoken.value})
    router.push('/hom')
  }finally{
    loading.value= false
  }

}

function handleIcons() {
  showPassword.value = !showPassword.value;
}
</script>

<style scoped>

.custom-icon {
  rotate: 180deg;
}

.full-width {
  width: 100%;
}
.custom-margin {
  margin-top: 40px;
}
.margin-input {
  margin-bottom: 24px;
}
.custom-border{
  border: 1px solid var(--orange-primary);
}
</style>
