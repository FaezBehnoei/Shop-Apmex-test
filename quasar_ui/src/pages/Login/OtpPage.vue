<template>
  <div class="main-container q-mx-auto">
    <form class="full-width" @submit.prevent="handleSubmit">
      <div class=" full-width">

        <!-- logo & inputs  -->
        <div class="flex column flex-center">
          <!-- back button  -->
         <div class="flex items-start full-width q-mb-md">
          <SvgIcon name="arrow-left" state="black" size="24" class="custom-icon" @click="router.go(-1)" cursor="true"/>
         </div>
          <!-- logos  -->
          <div class="flex column flex-center custom-margin">
            <img src="/icons/icon-color.png" :width="42" alt="monogram" class="q-mb-lg">
            <p class="typography-h4-bold h4-color">تایید شماره موبایل</p>
          </div>
          <!-- inputs  -->
          <div class="full-width">
            <p class="typography-body-lg-medium q-mb-md">کد تایید را وارد کنید.</p>
            <p class="typography-body-md-regular text-white-dark-hover q-mb-sm">کد تایید برای شماره <span class="phone-number">{{ phoneNumberTemporary }}</span> پیامک شد :</p>
            <router-link :to="previousRoute" class="typography-caption-lg-bold edit-number-btn ">ویرایش شماره موبایل</router-link>
            <div class="flex items-center justify-evenly otp-div">
              <input data-no-fa maxlength="1" v-for="(item,index) in otpDigits.length" :key="index" type="text" class="otp-inputs flex flex-center text-center bg-white-light-active" v-model="otpDigits[index]" ref="inputs" @input="moveToNext(index, $event)" @keydown.backspace="moveToPrev(index)">
            </div>
            <p class="typography-body-md-regular text-white-darker text-center custom-margin-code">
              <span v-if="expireOTP">{{ formattedTimer }} مانده تا ارسال کد مجدد</span>
              <button v-else @click="handleResendOtp" class="typography-body-md-medium reset-otp text-center text-blue-custom cursor-pointer">ارسال مجدد</button>
            </p>
            <div class="full-width">
              <ButtonComponent :loading="loading" size="lg" html-type="submit" label="تایید" type="primary" class="q-mb-lg full-width" :disable="isFilled"/>

            </div>
          </div>
        </div>

  </div>
    </form>
  </div>

</template>

<script setup>
import { useRouter,useRoute } from 'vue-router';
import { computed, nextTick, onMounted, ref } from 'vue';
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';
import { verifyOtp, verifyOtpResetPassword } from 'src/services/authService';

import ButtonComponent from 'src/components/ButtonComponent.vue';
import SvgIcon from 'src/components/SvgIcon.vue';

let timer = null
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const otpDigits = ref(Array(5).fill(""))
const inputs = ref([])
const isFilled = ref(true)
const loading = ref(false)
const otptoken = ref(authStore.otpToken || sessionStorage.getItem('otp_token'))
const phoneNumberTemporary = ref(sessionStorage.getItem('phone-temporary') || '')
const expireOTP = ref(parseInt(authStore.expireOTP || sessionStorage.getItem('expire_otp') || 0))
const flowType = route.query.flow

const isCompleted = computed(() => otpDigits.value.every(digit => digit != ""))

const previousRoute = computed(() => {
  const flow = route.query.flow
  if (flow === 'login') return '/auth/login'
  if (flow === 'signup') return '/auth/sign-up'
  if (flow === 'forgetPassword') return '/auth/create-password'
  return '/auth/login'
})

function focusOtpInputs(index){
  inputs.value[index]?.focus()
}
function moveToNext(index, event){
  if(event.target.value !== '' && index < inputs.value.length - 1 ){
    nextTick(() => {
      inputs.value[index+ 1].focus()
    })
  }
  if(isCompleted.value){
    isFilled.value = false
    handleSubmit()
  }
}
const formattedTimer = computed(() => {
  const minutes = Math.floor(expireOTP.value / 60).toString().padStart(2, '0')
  const seconds = (expireOTP.value % 60).toString().padStart(2, '0')
  return `${minutes}:${seconds}`
})


async function handleSubmit(){
  if (loading.value || !isCompleted.value) return;
  loading.value = true
  router.push('/home')
  try{
    if(flowType === 'login'){
      const response = await verifyOtp({otpCode: otpDigits.value.join(""), otpToken: otptoken.value})
      authStore.updateUserInfo(response.user_profile)
      authStore.clearPhoneNumber()
      authStore.removeOtpToken()
      router.push('/home')
    }else if(flowType === 'forgetPassword'){
      await verifyOtpResetPassword({otpCode: otpDigits.value.join(""), otpToken: otptoken.value})
      authStore.clearPhoneNumber()
      authStore.removeOtpToken()
      router.push('/auth/create-password')
    }else if(flowType === 'signup'){
      const  data  = await verifyOtp({otpCode: otpDigits.value.join(""), otpToken: otptoken.value})
      authStore.updateUserInfo(data.user_profile)
      authStore.clearPhoneNumber()
      authStore.removeOtpToken()
      router.push('/auth/create-user')
    }
  }catch{
    otpDigits.value = Array(5).fill("")
    nextTick(() => focusOtpInputs(0))
  }finally{
    loading.value = false
  }

}


function moveToPrev(index){
  inputs.value[index - 1].focus()
}

async function handleResendOtp(){
  try{
   const  data  =  await api.post('/auth/resend-otp', ({otp_token : otptoken.value}))
   expireOTP.value = data.expire_in
  }catch(err){
    console.log(err)
  }
}



onMounted(() => {
  focusOtpInputs(0)

  if (expireOTP.value > 0) {
    timer = setInterval(() => {
      if (expireOTP.value > 0) {
        expireOTP.value--
      } else {
        clearInterval(timer)
      }
    }, 1000)
  }
})




</script>

<style scoped>
.main-container{
  padding: 24px;
}

.custom-btn{
  background-color: transparent;
  border: none;
  color: rgba(175, 111, 34, 1);
  cursor: pointer;
}
.custom-margin{
  margin-bottom: 24px;
}

.custom-icon{
  rotate: 180deg;
}
.phone-number{
  font-weight: 700;
  font-size: 18px;
  line-height: 24px;
}
.edit-number-btn{
  display: inline-block;
  color: rgba(9, 12, 54, 1);
  border-bottom: 1px solid rgba(9, 12, 54, 1);
  margin-bottom: 40px;
}
.otp-inputs{
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid rgba(230, 230, 230, 1);
  color: rgba(81, 81, 81, 1);
  font-weight: 700;
  font-size: 18px;
  line-height: 24px;
  letter-spacing: 0%;
}
.otp-inputs:focus{
  outline: none;
}

.otp-div{
  direction: ltr !important;
}
.h4-color{
  color: rgba(12, 38, 71, 1);
}
.custom-margin-code{
  margin-top: 18px;
  margin-bottom: 40px;
}
.reset-otp{
  background-color: transparent;
  border: none;
  border-bottom: 1px solid var(--blue-custom);
}
</style>
