
<template>
  <q-page class="main-container q-mx-auto flex column justify-center items-center">
    <!-- carousel  -->
    <CarouselLoginComponenet class="q-pb-md carouselComponents"/>
     <!-- buttons  -->
   <div class="full-width">
     <ButtonComponent size="lg" type="primary" label="ورود" class="q-mb-sm full-width" @click="PushToLogin"/>
    <ButtonComponent size="lg" type="text" label="ثبت نام و احراز هویت" @click="PushToRegister"/>
   </div>
  </q-page>
</template>

<script setup>
import ButtonComponent from 'src/components/ButtonComponent.vue';
import CarouselLoginComponenet from 'src/components/CarouselLoginComponenet.vue';
import { useRouter } from 'vue-router';

const router = useRouter()

function PushToLogin(){
  router.push('/auth/login')
}
function PushToRegister(){
  router.push('/auth/sign-up')
}

</script>


<style scoped>
.main-container{
  max-width: 600px;
  padding: 2.5rem 1.125rem 2rem 1.125rem;
}
@media(max-height : 700px){
  .main-container{
    padding-top: 1rem;
  }

}

</style>
