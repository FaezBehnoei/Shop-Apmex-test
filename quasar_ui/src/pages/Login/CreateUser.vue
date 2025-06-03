<template>
  <div class="main-container q-mx-auto">
    <form @submit.prevent="handleSubmit">
      <div class="flex column justify-between custom-height item-center full-height">

        <!-- logo & inputs  -->
        <div class="flex column flex-center">
          <!-- back button  -->
         <div class="flex items-start full-width q-mb-md">
          <SvgIcon name="arrow-left" state="black" size="24" class="custom-icon" @click="$router.go(-1)" cursor="true"/>
         </div>
          <!-- logos  -->
          <div class="flex column flex-center custom-margin">
            <img src="/icons/icon-color.png" :width="42" alt="monogram" class="q-mb-lg">
            <p class="typography-h4-bold h4-color">تایید مشخصات و رمز عبور</p>
          </div>
          <!-- inputs  -->
          <div class="full-width">
            <p class="typography-body-lg-medium q-mb-sm">اطلاعات کاربر</p>
            <!-- userInfo  -->
            <div class="flex column userInfo">
              <div class="flex items-center justify-between">
                <span class="typography-body-md-light text-blue-custom">نام و نام خانوادگی :</span>
                <span class="typography-body-md-light text-blue-custom">{{ fisrtName }} {{ lastName }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="typography-body-md-light text-blue-custom">کدملی :</span>
                <span class="typography-body-md-light text-blue-custom">{{ nationalId }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="typography-body-md-light text-blue-custom">شماره همراه :</span>
                <span class="typography-body-md-light text-blue-custom">{{ phoneNumber }}</span>
              </div>
            </div>
            <!-- inputs  -->
             <div class="custom-mb">
              <InputComponent label="رمز عبورخود را وارد کنید:" placeholder="رمز عبور را وارد کنید." class="q-mb-md typography-caption-lg-regular" v-model="password" @keydown.enter.prevent="goToNextField" autoInput="true" :icon="icon" :type="type" state="black" Iconsize="16" @clicked-icon="handleIcon"/>
              <InputComponent label="کد دعوت (اختیاری)" placeholder="کد دوت را وارد کنید" class="q-mb-sm typography-caption-lg-regular" ref="codeInput" v-model="inviteCode" :error="inviteCodeError"/>
              <p v-if="inviteCodeError" class="text-negative typography-caption-lg-regular q-mt-sm">
                کد معرف معتبر نیست.
              </p>

             </div>
            <!-- button  -->
            <ButtonComponent size="lg" html-type="submit" label="تایید و ورود به برنامه" type="primary" class="q-mb-lg" />
          </div>
        </div>

  </div>
    </form>
  </div>

</template>

<script setup>
import { useRouter } from 'vue-router';
import { computed, ref, watch } from 'vue';
import { useAuthStore } from 'src/stores/auth';
import debounce from 'lodash.debounce';

import ButtonComponent from 'src/components/ButtonComponent.vue';
import SvgIcon from 'src/components/SvgIcon.vue';
import InputComponent from 'src/components/InputComponent.vue';
import { completeSignup,validateInviteCode } from 'src/services/authService';

const router = useRouter()
const codeInput = ref('')
const showPassword = ref(true)
const password = ref('')
const inviteCode = ref('')
const authStore = useAuthStore()
const inviteCodeError = ref(false)
const fisrtName = authStore.userInfo.firstName
const lastName = authStore.userInfo.lastName
const nationalId = authStore.userInfo.nationalId
const phoneNumber = authStore.userInfo.phoneNumber


const icon = computed(() => showPassword.value ? 'eye' : 'close-eye')
const type = computed(() => showPassword.value ? 'password' : 'text')

function handleIcon(){
  showPassword.value = !showPassword.value
}

async function handleSubmit(){
  await completeSignup({password:password.value, inviteCode: inviteCode.value,phoneNumber: phoneNumber || null })
  router.push('/home')
}
function goToNextField(event){
  event.preventDefault();
  codeInput.value.focus()
}

const checkInviteCode = debounce(async(code) => {
  if(!code || code.length < 4) return;

  try{
    const  data  =  await validateInviteCode({inviteCode: code})
    if(data.valid){
      inviteCodeError.value = false
    }
  }catch(err){
    inviteCodeError.value = true
    console.log(err)
  }
}, 800)

watch(inviteCode, (newCode) => {
  inviteCodeError.value = false
  checkInviteCode(newCode)
})




</script>

<style scoped>
.main-container{
  height: 100vh;
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
.custom-height{
  max-height: 706px;
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
.userInfo{
  border-radius: 8px;
  border-width: 1px;
  gap: 8px;
  padding-top: 8px;
  padding-bottom: 8px;
  background-color: rgba(246, 250, 255, 1);
  margin-bottom: 40px;
}
.userInfo > div{
  padding: 13px 16px;
}
.custom-mb{
  margin-bottom: 40px;
}
</style>
