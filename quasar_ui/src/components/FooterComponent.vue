<template>
  <div class="main-container-footer q-mx-auto flex flex-center">
    <ul class="flex justify-between items-center ul-style full-width">
      <li class="flex column items-center" v-for="item in List" :key="item.id" @click="handleListItems(item)">
        <SvgIcon :name="active === item.title ? item.activeIcon : item.icon" state="black" size="24" class="text-color-red q-mb-xs"/>
        <span :class="active === item.title ? 'selected-item' : 'text-white-dark-active'" class="typography-caption-md-regular items-style">{{ item.title }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import SvgIcon from './SvgIcon.vue';
import { useRouter, useRoute } from 'vue-router';

const active = ref('')
const router = useRouter()
const route = useRoute()

const List = ref([
  {id:1, icon:'goldis-footer', activeIcon: 'home-active', title:'خانه', route:'/home'},
  {id:2, icon:'wallet', activeIcon: 'wallet-active', title:'دارایی ها', route:'/account/wallet'},
  {id:3, icon:'shop', activeIcon: 'shop-active', title:'فروشگاه', route:'/home/shop'},
  {id:4, icon:'profile', activeIcon: 'profile-active', title:'پروفایل', route:'/home/profile'},
])

function handleListItems(item){
  active.value = item.title;
  router.push(item.route)
}

function syncActiveWithRoute(){
  const found = List.value.find(item => route.path === item.route)
  active.value = found?.title || null
}

onMounted(syncActiveWithRoute)
watch(() => route.path, syncActiveWithRoute)
</script>

<style scoped>
.main-container-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  border-top: 1px solid var(--white-normal);
  background-color: var(--white-light);
  height: 3.75rem; /* 60px */
  z-index: 100;
}

.main-container-footer:hover {
  background-color: var(--white-light-hover);
}

.ul-style {
  padding: 0.5rem 1rem;
  margin: 0;
  cursor: pointer;
}
.items-style{
  padding: 0.125rem 0.95rem;
}

.selected-item {
  background-color: rgba(12, 38, 71, 0.1);
  padding: 0.125rem 0.95rem; /* 2px 4px */
  border-radius: 0.5rem; /* 8px */
  color: var(--blue-custom);
}
</style>

