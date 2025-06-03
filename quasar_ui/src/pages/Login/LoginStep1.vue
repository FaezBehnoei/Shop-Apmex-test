<template>
  <div class="main-container q-mx-auto">
    <form @submit.prevent="handleSubmit" class="full-height full-width flex column">

      <!-- logo + title -->
      <div class="flex column items-center">
        <img src="../../assets/monograms/Property 1=monogram_color 2_48px.svg" alt="monogram" width="42" class="q-mb-md" />
        <p class="typography-h4-bold text-blue-custom q-mb-md q-mt-sm q-pb-sm">ورود به گلدیس</p>

        <!-- inputs -->
        <div class="full-width q-mt-md">
         <div class="full-width flex column items-center margin-bottom-input">
          <InputComponent
            v-model="phoneNumber"
            label="کد ملی یا شماره موبایل"
            placeholder="شماره موبایل یا کد ملی خود را وارد کنید."
            class="typography-caption-lg-regular q-mb-md"
            :autoInput="true"
            @keydown.enter.prevent="goToNextField"
            :rules="[rules.required]"
            size="xl"
          />
          <InputComponent

            :stateInput="password ? 'fill' : ''"
            label="رمز عبور"
            placeholder="رمز عبور خود را وارد کنید."
            v-model="password"
            :type="type"
            :icon="icon"
            state="black"
            :custom-class-icon="iconClass"
            Iconsize="16"
            @clicked-icon="handleIcons"
            ref="passInput"
            class="typography-caption-lg-regular no-persian-convert"
          />


         </div>
          <!-- extra buttons -->
          <div class="flex column items-start">
            <button @click="handleOTPMethod" type="button" class="link-btn typography-caption-lg-medium text-blue-custom q-mb-sm">ورود با رمز یکبار مصرف</button>
            <button @click="handleForgetPass" type="button" class="link-btn typography-caption-lg-medium text-blue-custom">فراموشی رمز عبور</button>
          </div>
        </div>
      </div>

      <!-- main button + sign up -->
      <div class="flex column items-center custom-margin">
        <ButtonComponent
          :disable="!isFormValid"
          :loading="loading"
          size="lg"
          html-type="submit"
          label="ورود با رمز عبور"
          type="primary"
          class="q-mb-md bg-orange-primary text-blue-custom full-width margin-input"
        />
        <div class="flex items-center">
          <span class="typography-body-md-regular">حساب کاربری ندارید؟</span>
          <router-link to="/auth/sign-up" class="typography-body-md-bold signup-link q-mr-xs">
            ثبت نام
          </router-link>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import {rules} from 'src/utils/rules'

import ButtonComponent from 'src/components/ButtonComponent.vue';
import InputComponent from 'src/components/InputComponent.vue';
import { useAuthStore } from 'src/stores/auth';
import { handleError, loginWithPassword, requestOtp, requestOtpFogrgetPassword } from 'src/services/authService';
import { showSuccess } from 'src/utils/toast';

const router = useRouter()
const authStore = useAuthStore()


const password = ref('')
const phoneNumber = ref(authStore.phoneNumberTemporary || '')

const loading = ref(false)

const showPassword = ref(false)


const type = computed(() => (showPassword.value ? 'text' : 'password'))
const icon = computed(() => (showPassword.value ? 'close-eye' : 'eye'))
const iconClass = computed(() => (showPassword.value ? 'text-black' : ''))


const passInput = ref(null)
function goToNextField(event) {
  event.preventDefault();
  passInput.value?.focus();
}

const isFormValid = computed(() =>
  phoneNumber.value.trim() !== '' && password.value.trim() !== ''
)




function handleIcons() {
  showPassword.value = !showPassword.value;
}

async function handleSubmit() {
  if (loading.value) return;
  loading.value = true
  try{
    await loginWithPassword({identifier: phoneNumber.value, password: password.value})
    showSuccess('با موفقیت وارد شدید')
    router.push('/home');
  }catch(err){
    handleError(err)
  }finally{
    loading.value = false
  }

}

async function handleOTPMethod() {
  if(rules.required(phoneNumber.value) !== true) return;

  try{
    const  data  = await requestOtp({phoneNumber: phoneNumber.value})
    authStore.setPhoneNumberTemporary(phoneNumber.value)
    authStore.setOtpToken(data.otp_token)
    authStore.setExpireOTP(data.expires_in)
    router.push('/auth/otp?flow=login')
  }catch(err){
    handleError(err)
  }
}
async function handleForgetPass() {
  if(rules.required(phoneNumber.value) !== true) return;

  try{
    const  data  = await requestOtpFogrgetPassword({phoneNumber: phoneNumber.value})
    authStore.setPhoneNumberTemporary(phoneNumber.value)
    authStore.setOtpToken(data.reset_token)
    authStore.setExpireOTP(data.expires_in)
    router.push('/auth/otp?flow=forgetPassword')
  }catch(err){
    handleError(err)
  }
}
</script>

<style scoped>
.main-container {
  padding: 64px 24px 72px 24px;
}

.link-btn {
  background: transparent;
  border: none;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  border-bottom: 0.5px solid var(--blue-custom);
}

.full-width {
  width: 100%;
}
.custom-margin{
  margin-top: 40px;
}
.margin-input{
  margin-bottom: 24px;
}
.signup-link{
  color: var(--orange-primary);
}
.margin-bottom-input{
  margin-bottom: 10px;
}
</style>
