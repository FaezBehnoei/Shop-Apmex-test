import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProfile, getProfileEdit,submitProfileEdit, getProfileNotifications } from 'src/services/profileServices'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const profileEdits = ref({})
  const unreadNotificationCount = ref(0)

  // اطلاعات پروفایل را از API می‌گیرد
  async function fetchProfile() {
    const data = await getProfile()
    profile.value = data
  }

  // edit profile informations
  async function getProfileEditInfo() {
    const data = await getProfileEdit()
    profileEdits.value = data
  }
  // set profile Fields
  function setProfileField(field, value) {
  if (profileEdits.value) {
    profileEdits.value[field] = value
  }
}
  // edit profile informations
  async function submitProfileEditInfo() {
    await submitProfileEdit(profileEdits.value)
  }



  // چک کردن تعداد نوتیف‌های خوانده‌نشده
  async function fetchUnreadNotifications() {
    const data = await getProfileNotifications()
    unreadNotificationCount.value = data.filter(n => !n.isRead).length
  }

  // ریست کردن نوتیف‌ها بعد از خواندن
  function clearUnreadNotifications() {
    unreadNotificationCount.value = 0
  }

  return {
    profile,
    profileEdits,
    unreadNotificationCount,
    fetchProfile,
    setProfileField,
    fetchUnreadNotifications,
    clearUnreadNotifications,
    getProfileEditInfo,
    submitProfileEditInfo
  }
})
