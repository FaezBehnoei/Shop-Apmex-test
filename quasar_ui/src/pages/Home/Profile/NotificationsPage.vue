<template>
  <q-page class="q-mx-md">
    <BannerDashboard />
    <div class="q-mt-md">
      <div v-if="!notifications.length" class="text-center">نوتیف جدیدی ندارید.</div>
      <div v-for="note in notifications" :key="note.id">
        <NotificationsComponent
          :title="note.title"
          :message="note.message"
          :timestamp="note.timestamp"
          :isRead="note.isRead"
          :id="note.id"
          @notif-opened="handleNotificationIsread"
        />
      </div>
  </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import BannerDashboard from 'src/components/Home/bannerDashboard.vue';
import NotificationsComponent from 'src/components/profile/NotificationsComponent.vue';
import { getProfileNotifications, getProfileMarkNotificationsRead } from 'src/services/profileServices';
import { useProfileStore } from 'src/stores/profileStore';

const notifications = ref([])
const readIds = new Set()

const profileStore = useProfileStore()
async function loadNotifications() {
  const  data  = await getProfileNotifications()    // GET /notifications
  notifications.value = data
}


onMounted(async () => {
  await loadNotifications()
})



function handleNotificationIsread(id) {
  const notif = notifications.value.find(n => n.id === id)
  if (notif && !notif.isRead) {
    notif.isRead = true
    profileStore.unreadNotificationCount--   // sync UI
    readIds.add(id)
  }
}
onBeforeUnmount(async () => {
  if (readIds.size) {
    await getProfileMarkNotificationsRead([...readIds])
    await profileStore.fetchUnreadNotifications() 
  }
})






</script>

