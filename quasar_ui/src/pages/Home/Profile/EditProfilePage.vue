<template>
  <q-page class="q-px-md q-py-sm">
    <div class="flex">
      <div class="typography-subtitle-medium flex flex-center">
        <div class="circle-div flex flex-center text-center"></div>
        <span class="q-mr-sm">اطلاعات فردی</span>
      </div>
    </div>
    <div>
      <ProfileFormComponent v-for="(item, index) in profileFields" :key="item.key"
        :label="item.label"
        v-model="item.model"
        :placeholder="item.placeholder"
        :icon="item.icon"
        :type="item.type"
        :options="item.options"
        ref="fieldRefs"
        @focus-next="focusNext(index)"
        @updated="handleGetInfoAgain"
      />
    </div>
  </q-page>
</template>

<script setup>
import ProfileFormComponent from 'src/components/profile/profileFormComponent.vue';
import { computed, onMounted, ref, watch } from 'vue';
import { useProfileStore } from 'src/stores/profileStore';

const profileStore = useProfileStore()
const profileData = computed(() => (profileStore?.profileEdits))



const fieldRefs = ref([])


function focusNext(currentIndex) {
  const focusables = Array.from(
    document.querySelectorAll('.form-input, .dropdown-header')
  )

  const next = focusables[currentIndex + 1]
  if (next && typeof next.focus === 'function') {
    next.focus()
  }
}
const profileFields = ref([])
function generateProfileFields(profileData) {
  return [
    {
      key:'full_name',
      label: 'نام و نام خانوادگی',
      model: profileData.full_name || '',
      type: 'input'
    },
    {
      key:'national_id',
      label: 'کد ملی',
      model: profileData.national_id || '',
      type: 'input'
    },
    {
      key:'phone_number',
      label: 'شماره همراه',
      model: profileData.phone_number || '',
      type: 'input',
      icon: true,
      editable: true
    },
    {
      key:'password',
      label: 'رمز عبور',
      model: profileData.password || '',
      type: 'input',
      icon: true,
      editable: true
    },
    {
      key:'gender',
      label: 'جنسیت',
      model: profileData.gender || '',
      type: 'select',
      placeholder: profileData.gender || '',
      options: ['مرد', 'زن'],
      dropdown: true
    },
    {
      key:'connection',
      label: 'نحوه آشنایی',
      model: profileData.referral_source || '',
      type: 'select',
      placeholder: 'انتخاب کنید',
      options: ['گوگل', 'اینستاگرام', 'دوست', 'سایر'],
      dropdown: true
    },
    {
      key:'email',
      label: 'ایمیل',
      model: profileData.email || '',
      type: 'input'
    }
  ]
}


onMounted(async() => {
  await profileStore.getProfileEditInfo()
  profileFields.value = generateProfileFields(profileData.value)

})
watch(profileData, (newVal) => {
  if (newVal) {
    profileFields.value = generateProfileFields(newVal)
    console.log(profileFields.value)
  }
})

async function handleGetInfoAgain() {
  await profileStore.getProfileEditInfo()
  profileFields.value = generateProfileFields(profileData.value)
}


</script>

<style scoped>
.circle-div{
  background-color: var(--orange-primary);
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
}
</style>
