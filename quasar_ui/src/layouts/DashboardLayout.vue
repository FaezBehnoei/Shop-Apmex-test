<template>
  <q-layout view="lHh Lpr lFf">

     <!-- header  -->
    <div class="flex items-center justify-between q-px-md q-py-sm">
      <div>
        <img src="/images/logo (1).svg" alt="گلدیس">
      </div>
      <div class="flex items-center justify-between">
        <div class="icon-wrapper flex flex-center q-ml-sm">
          <SvgIcon name="shop-cart" state="black" size="24" />
        </div>
        <div @click="router.push('/account/notifications')" class="icon-wrapper cursor-pointer flex flex-center">
          <SvgIcon name="notif" state="black" size="24"/>
          <div v-if="hasUnreadNotifications" class="notif-indicator"></div>
        </div>
      </div>
    </div>

    <q-page-container>
      <router-view />
    </q-page-container>

    <FooterComponent />
  </q-layout>
</template>

<script setup>
import { useRouter } from 'vue-router';
import SvgIcon from 'src/components/SvgIcon.vue';
import FooterComponent from 'src/components/FooterComponent.vue';
import {  computed, onMounted } from 'vue';
import { useProfileStore } from 'src/stores/profileStore';

const router = useRouter()
const profileStore = useProfileStore()
const hasUnreadNotifications = computed(() => profileStore.unreadNotificationCount > 0)


async function checkUnread() {
  await profileStore.fetchUnreadNotifications()
}

onMounted(() => {
  checkUnread()
})


</script>

<style scoped>
.icon-wrapper {
  position: relative;
  padding: 0.625rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(222, 222, 222, 1);
}
.notif-indicator {
  position: absolute;
  top: 14px;
  right: 12px;
  width: 7px;
  height: 7px;
  background-color: #FF0000FA;
  border-radius: 50%;
}

</style>
