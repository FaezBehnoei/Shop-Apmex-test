<template>
  <q-page class="q-px-md q-pb-md">
    <div class="">
      <div class="q-px-md q-pt-sm flex column" v-for="item in informations" :key="item.title">
        <span class="typography-body-lg-bold q-py-md">{{ item.title }}</span>
        <div class="typography-body-md-regular">{{ item.description }}</div>
      </div>
    </div>
    <div class="q-px-md">
      <div class="typography-body-lg-bold q-py-md">مجوز ها </div>
      <div class="flex justify-evenly">
        <div class="flex flex-1 column items-center justify-center" v-for="permit in permits" :key="permit.title">
          <img class="q-mb-xs" :src="permit.image" :alt="permit.title">
          <span class="q-mb-sm">{{ permit.title }}</span>
        </div>
      </div>
    </div>
    <div class="q-px-md">
      <div class="typography-body-lg-bold q-pt-md" > تماس با ما</div>
      <contactUsFooter />
    </div>
    <div class="social-section q-mt-lg">
      <div class="typography-body-md-bold text-center q-mb-md">
        ما را در شبکه های اجتماعی دنبال کنید
      </div>
      <div class="flex justify-center q-gutter-sm">
        <div
          v-for="item in socialIcons"
          :key="item.name"
          class="social-icon-wrapper"
        >
          <img :src="item.icon" :alt="item.name" class="social-icon" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import contactUsFooter from 'src/components/profile/contactUsFooter.vue';

const informations = ref([
  {title : 'درباره گلدیس', description: 'لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو '},
  {title : 'درباره گلدیس', description: 'لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو '},
])

const permits = ref([
  {title:'انفورماتیک', image:'/images/PermitsProfile.svg'},
  {title:'نظام صنفی', image:'/images/PermitsProfile.svg'},
  {title:'اتاق بازرگانی', image:'/images/PermitsProfile.svg'},
  {title:'اتحادیه طلا', image:'/images/PermitsProfile.svg'},
])
const socialIcons = [
  { name: 'نماد ۱', icon: '/images/social-1.svg' },
  { name: 'نماد ۲', icon: '/images/social-2.svg' },
  { name: 'نماد ۳', icon: '/images/social-3.svg' },
  { name: 'نماد ۴', icon: '/images/social-4.svg' }
]
</script>

<style lang="css" scoped>
.social-section {
  color: rgba(92, 92, 92, 1);
  margin-bottom: 2rem;
}

.social-icon-wrapper {
  border: 1px solid var(--orange-primary);
  border-radius: 8px;
  padding: 6px;
  background-color: #fff;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.social-icon {
  width: 20px;
  height: 20px;
}
</style>
