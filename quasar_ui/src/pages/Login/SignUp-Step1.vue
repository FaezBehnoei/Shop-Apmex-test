<template>
  <div class="main-container flex q-mx-auto">
    <form @submit.prevent="handleSubmit" class="full-height full-width flex column">

      <!-- logo + title -->
      <div class="flex column items-center">
        <img src="../../assets/monograms/Property 1=monogram_color 2_48px.svg" alt="monogram" width="42" class="q-mb-md" />
        <p class="typography-h4-bold text-blue-custom q-mb-md q-mt-sm q-pb-sm logo-margin-bottom">ثبت نام و احراز هویت</p>


         <!-- error message -->
         <div v-if="error" class="flex row q-pl-md q-mt-sm">
          <div class="typography-body-md-regular text-negative">
            * {{ errorMessage || 'کد ملی و شماره موبایل وارد شده با یکدیگر مغایرت دارند.' }}
          </div>
         </div>
         <!-- inputs -->
        <div class="full-width flex column flex-center q-mt-md">
          <InputComponent
            label="کد ملی"
            placeholder="کد ملی خود را وارد کنید."
            class="q-mb-md typography-caption-lg-regular"
            v-model="nationalId"
            :autoInput="true"
            @keyup.enter="goToNextInput"
            :error="error ? true : false"
          />
          <InputComponent
            label="شماره موبایل"
            placeholder="شماره موبایل خود را وارد کنید."
            class="q-mb-sm  typography-caption-lg-regular"
            v-model="phoneNumber"
            ref="inputPhone"
            :error="error ? true : false"
          />

          <!-- agree to terms -->
          <div class="flex items-center full-width max-width q-pa-xs q-mt-sm">
            <input  type="checkbox" class="checkbox q-ml-xs" v-model="agree" />
            <p class="typography-body-md-regular q-mb-none text-blue-custom">
              قوانین و مقررات را می پذیرم.
            </p>
          </div>

        </div>
      </div>

      <!-- main button + login link -->
      <div class="flex column items-center custom-margin">
        <ButtonComponent
          html-type="submit"
          size="lg"
          label="ورود با رمز عبور"
          type="primary"
          :disable="!agree || loading"
          class="q-mb-md bg-orange-primary text-blue-custom full-width margin-input"
        />
        <div class="flex items-center justify-center q-pl-md full-width">
          <span class="typography-body-md-regular">حساب کاربری دارید؟</span>
          <router-link to="/auth/login" class="typography-body-md-bold signup-link q-pr-xs">
            ورود
          </router-link>
        </div>
      </div>

    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import ButtonComponent from 'src/components/ButtonComponent.vue';
import InputComponent from 'src/components/InputComponent.vue';
import { verifyNationalIdAndPhone } from 'src/services/authService';
import { useAuthStore } from 'src/stores/auth';

const router = useRouter();
const nationalId = ref(sessionStorage.getItem('nationalId-temporary') || '');
const phoneNumber = ref(sessionStorage.getItem('phone-temporary') || '');
const agree = ref(false);
const inputPhone = ref(null);
const error = ref(false);
const errorMessage = ref('');
const loading = ref(false);
const authStore = useAuthStore();

function goToNextInput() {
  inputPhone.value?.focus();
}

async function handleSubmit() {
  if (!agree.value) return;

  // Reset error state
  error.value = false;
  errorMessage.value = '';
  loading.value = true;

  try {
    const response = await verifyNationalIdAndPhone({
      phoneNumber: phoneNumber.value,
      nationalId: nationalId.value
    })


    authStore.setExpireOTP(response.expires_in)
    authStore.setOtpToken(response.otp_token)
    authStore.setPhoneNumberTemporary(phoneNumber.value)
    authStore.setNationalIdTemporary(nationalId.value)



    router.push('/auth/otp?flow=signup')

  } catch (err) {
    console.error('خطا در ارسال درخواست:', err);
    error.value = true;

    if (err.response && err.response.data) {
      console.log('جزئیات خطا:', err.response.data);

      const errorKey = err.response.data.detail || err.response.data.message;
      errorMessage.value = errorKey ? (errorMessageMap[errorKey] || 'خطایی رخ داده است') : 'خطایی رخ داده است';
    } else {
      errorMessage.value = 'خطا در ارتباط با سرور. لطفا دوباره تلاش کنید.';
    }
  } finally {
    loading.value = false;
  }
}

// Import error message map directly to use in component
const errorMessageMap = {
  'Invalid credentials': 'نام کاربری یا رمز عبور اشتباه است.',
  'OTP expired': 'کد تایید منقضی شده است.',
  'OTP incorrect': 'کد تایید اشتباه است.',
  'National ID and phone number do not match': 'کد ملی و شماره همراه مطابقت ندارند.',
  'Invite code is invalid': 'کد دعوت نامعتبر است.',
  'User not found': 'کاربری با این مشخصات یافت نشد.',
  'Password too weak': 'رمز عبور باید حداقل ۸ کاراکتر و شامل عدد و حرف باشد.',
};
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

.checkbox {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  appearance: none;
  -webkit-appearance: none;
  border: 1px solid var(--orange-primary);
  background: transparent;
  position: relative;
  cursor: pointer;
}

.checkbox:checked {
  background-color: var(--orange-primary);
  border-color: var(--orange-primary);
}

.checkbox:checked::after {
  content: "";
  position: absolute;
  top: 2px;
  right: 4px;
  width: 4px;
  height: 8px;
  border-right: 2px solid white;
  border-bottom: 2px solid white;
  transform: rotate(45deg);
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
.signup-link {
  color: var(--orange-primary);
}
</style>
