<template>
  <div class="contact-footer q-mt-md">
    <div v-for="item in aboutUs" :key="item.title" class="contact-item">
      <span class="typography-body-md-regular value">{{item.title}} : {{item.description}}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const aboutUs = ref([
  {title: 'ایمیل', description: 'nemidonam@gmail.com'},
  {title: 'وب‌سایت', description: 'goldis.ir'},
  {title: 'آدرس', description: 'لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپه و با استفاده از طراحان گرافیک است.'},
])
</script>

<style scoped>
.contact-footer {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contact-item {
  display: flex;
  flex-wrap: wrap;
}



.value {
  color: rgba(92, 92, 92, 1);
}
</style>
