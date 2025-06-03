import { defineStore } from "pinia";
import { ref, reactive } from "vue";
import { api } from "src/boot/axios";


export const useAuthStore = defineStore('auth',() => {
  const isAuthenticated = ref(false);
  const phoneNumberTemporary = ref(sessionStorage.getItem('phone-temporary') || '')
  const nationalIdtemporary = ref(sessionStorage.getItem('id-temporary') || '')
  const otpToken = ref(sessionStorage.getItem('otp_token') || '')
  const expireOTP = ref(sessionStorage.getItem('expire_otp') || '')

  const userInfo = reactive({
    firstName: '',
    lastName: '',
    password: '',
    phoneNumber: '',
    nationalId: '',
    userId: '',
    rialBalance: '',
    goldBalance: '',
  });

  const isInitialized = ref(false);
  const checkAuth = async () => {
    try {
      const { data } = await api.get('/auth/is-authenticated');

      if (data.authenticated) {
        isAuthenticated.value = true;
        updateUserInfo(data.user_profile)
      } else {
        isAuthenticated.value = false;
        clearUserInfo();
      }

      isInitialized.value = true;
    } catch (error) {
      console.error('🔴 Authentication check failed:', error);
      isAuthenticated.value = false;
      clearUserInfo();

      isInitialized.value = false;
    }
  };

  const setPhoneNumberTemporary = (number) => {
    phoneNumberTemporary.value = number
    sessionStorage.setItem('phone-temporary', number)
  }

  const setNationalIdTemporary = (id) => {
    nationalIdtemporary.value = id
    sessionStorage.setItem('id-temporary', id)
  }

  const clearPhoneNumber = () => {
    phoneNumberTemporary.value = ''
    nationalIdtemporary.value = ''
    sessionStorage.removeItem('id-temporary')
    sessionStorage.removeItem('phone-temporary')
  }



  const setOtpToken = (token) => {
    otpToken.value = token
    sessionStorage.setItem('otp_token',otpToken.value)
  }
  const removeOtpToken = () => {
    sessionStorage.removeItem('otp_token')
  }

  const setExpireOTP = (time) => {
    expireOTP.value = time
    sessionStorage.setItem('expire_otp',setExpireOTP)
  }

  const removeExpireOtp = () => {
    sessionStorage.removeItem('expire_otp')
  }

  const updateUserInfo = (userData) => {
    Object.assign(userInfo, {
      firstName : userData.first_name || '',
      lastName : userData.last_name || '',
      password : userData.password || '',
      phoneNumber : userData.phone_number || '',
      nationalId : userData.national_id || '',
      userId : userData.id || '',
      rialBalance : userData.rial_balance || '',
      goldBalance : userData.gold_balance || '',
      })
  };



  const clearUserInfo = () => {
    Object.assign(userInfo, {
      firstName: '',
      lastName: '',
      password: '',
      phoneNumber: '',
      nationalId: '',
      userId: '',
      rialBalance: '',
      goldBalance: ''
    });
    isAuthenticated.value = false;
  };


  const logout = async () => {
    try {
      await api.post('/logout');
      localStorage.clear()
    } catch (error) {
      console.error('🚨 Logout error:', error);
    } finally {
      isAuthenticated.value = false;
      isInitialized.value = false;
      clearUserInfo();
    }
  };


  return {
    isAuthenticated,
    userInfo,
    otpToken,
    expireOTP,
    phoneNumberTemporary,
    nationalIdtemporary,
    setOtpToken,
    removeOtpToken,
    checkAuth,
    logout,
    updateUserInfo,
    clearUserInfo,
    setPhoneNumberTemporary,
    setNationalIdTemporary,
    clearPhoneNumber,
    setExpireOTP,
    removeExpireOtp,
  }
})
