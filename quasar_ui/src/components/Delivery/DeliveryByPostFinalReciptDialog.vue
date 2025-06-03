<template>
  <q-page v-if="props.modalValue" class="container">

    <!-- Header -->
      <div class="flex items-center page-header">
      <button @click="router.back()" class="back-btn">
        <SvgIcon class="back-icon" name="navbar-up" state="black" size="24"  cursor="true"/>
      </button>
      <div class="full-width text-center">
          <span class="typography-body-lg-bold flex flex-center text-blue-custom">تحویل با پیک</span>
        </div>
      </div>
    <div class="card">


      <!-- Content -->
      <div class="content">
        <!-- header  -->
         <div class="flex flex-center inside-header">
          <SvgIcon name="transfer-motorcycle" state="black" size="32" class="driving-icon"/>
          <span class="typography-body-lg-medium ">تحویل با پیک</span>
          <SvgIcon name="transfer-motorcycle" state="transparent" size="24" style="visibility: hidden;" />

         </div>
         <!-- devider  -->
          <div class="divider-wrapper">
          <span class="circle left"></span>
          <div class="divider-line"></div>
          <span class="circle right"></span>
        </div>

        <div class="q-px-md content-inside">
          <div class="order-number typography-body-lg-medium">سفارش <span class="text-positive">{{ orderId }}</span></div>

          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">تاریخ:</div>
              <div class="typography-body-md-regular text-grey-normal">{{ props.timing.date }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">روز:</div>
              <div class="typography-body-md-regular text-grey-normal">{{ props.timing.day }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">ساعت:</div>
              <div class="typography-body-md-regular text-grey-normal">{{ props.timing.time }}</div>
            </div>
          </div>

          <div class="address">
            <div class="typography-caption-lg-regular text-white-darker">آدرس:</div>
            <div class="typography-caption-lg-regular text-grey-normal">{{ address.address }}</div>
          </div>

          <div class="phone">
            <div class="typography-body-md-regular text-grey-normal">0{{ phone }}</div>
            <div class="typography-caption-lg-regular text-white-darker">شماره همراه پیک:</div>
          </div>
        </div>

        <div class="q-px-sm">
         <ButtonComponent label="تایید" type="primary" size="lg" @click="handleConfirm" />

        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { useRouter } from 'vue-router';
import SvgIcon from 'src/components/SvgIcon.vue';
import ButtonComponent from '../ButtonComponent.vue';
const props = defineProps({
  modalValue: { type : Boolean , required : true},
  orderId: { type: Number, default: 123445 },
  timing : { type : Object},
  address: {
    type: Object,
    required: true,
    default: () => ({
    })
  },
  phone: { type: Number, default: 9123452431 }
})

const emit = defineEmits(['confirm'])
const router = useRouter()

function handleConfirm() {
  emit('confirm')
}
</script>

<style scoped>
.container {
  background-color: white;
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
}

.card {
  background-color: white;
  padding-inline: 1rem;
  overflow: hidden;
}

.inside-header{
  padding: 1.5rem;
}


.header::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 0;
  right: 0;
  height: 20px;
  background-color: #f3f3f3;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
}
.divider-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-inline: -1.6rem;
}

.divider-line {
  flex: 1;
  border-top: 1px dashed var(--white-normal-hover); /* یا رنگ دلخواه */
  height: 1px;
}

.circle {
  width: 2.625rem;
  height: 2.3125rem;
  background-color: white;
  border-radius: 50%;
  z-index: 1;
}

.circle.left {
  margin-left: -1rem; /* نصف شعاع */
}

.circle.right {
  margin-right: -1rem;
}



.title {
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  display: flex;
  align-items: center;
  gap: 8px;
}

.content {
  background-color: var(--white-light-active);
  border-radius: 1.25rem;
  padding-bottom: 2rem;

}


.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 3rem;
  margin-bottom: 1.3rem;
  margin-top: 0.5rem;
  align-items: center;
  margin-inline: auto;
}

.info-item {
  text-align: right;
}

.info-label {
  font-weight: 400;
  font-size: 0.75rem;
  line-height: 1.125rem;
  color: var(--white-darker);
  margin-bottom: 0.25rem;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
}

.address {
  margin-bottom: 1.9rem;
}


.phone {
  direction: ltr;
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}


.page-header {
  position: relative;
  height: 3rem;           /* 48px */
  padding: 0 1rem;        /* 16px */
  margin-bottom: 1rem;
}

.page-header .back-icon {
  position: absolute;
  right: 1rem;            /* 16px */
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.back-btn {
  outline: none;
  border: none;
}
.driving-icon{
  background-color: #FFEFE5;
  border-radius: 4px;
  margin-left: 0.1rem;

}
</style>
