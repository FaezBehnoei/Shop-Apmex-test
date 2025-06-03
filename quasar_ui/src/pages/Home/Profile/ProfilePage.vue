<template>
  <q-page class="q-px-md q-py-sm">

    <div class="q-py-sm">
      <!-- Profile Info -->
      <div class="profile-box q-pb-sm">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <img src="/images/profileImg.png" alt="img" />
            <div>
              <div class="q-mr-sm typography-body-lg-medium">{{ profile?.fullName }}</div>
              <div class=" q-mr-sm typography-body-md-medium text-right q-mt-xs text-white-dark-hover">{{ profile?.mobile }}</div>
            </div>

          </div>
          <div class="flex">
            <div v-if="profile?.verified" class="badge typography-caption-md-regular">احراز هویت شده</div>
            <div v-else class="badge-false typography-caption-md-regular">احراز هویت نشده</div>

            <button @click="router.push('/account/edit')" class="custom-btn flex flex-center">
              <SvgIcon class="cursor-pointer" name="arrow" state="black" size="24" />
            </button>
          </div>
        </div>
      </div>

      <!-- Wallet Summary -->
      <div class="wallet-summary q-mt-md row items-center justify-evenly">
        <div class="wallet-box col-5 text-center q-py-sm">
          <div class="typography-body-md-medium q-mb-sm">{{ formatNumber(profile?.assets) }} <span class="text-caption">ریال</span></div>
          <div class="text-white-dark-hover typography-caption-lg-light flex flex-center"><span class="flex flex-center">
            <SvgIcon name="wallet" state="black" size="16"/>
            <span class="q-mr-xs">دارایی شما</span>
          </span></div>
        </div>
        <div class="wallet-box col-5 text-center q-py-sm">
          <div class="typography-body-md-medium q-mb-sm">{{ formatNumber(profile?.total_profit) }} <span class="text-caption">ریال</span></div>
          <div class="text-white-dark-hover typography-caption-lg-light flex flex-center"><span  class="flex flex-center">
            <SvgIcon name="ignot" state="black" size="16" />
            <span class="q-mr-xs">مقدار سود کلی شما </span>
          </span></div>
        </div>
      </div>
    </div>

    <!-- Menu Items -->
    <div class="menu-list">
      <MenuItem icon="order-profile" label="تاریخچه سفارشات" route="/account/history"/>
      <MenuItem icon="add-user-profile" label="دعوت از دوستان" route="/account/invite-friends" />
      <MenuItem icon="wallet-profile" label="شماره شبا" route="/account/BankCard"/>
      <MenuItem icon="location-profile" label="آدرس ها"  route="/account/address"/>
      <MenuItem icon="contact-us-profile" label="پشتیبانی" />
      <MenuItem icon="about-us-profile" label="درباره ما" route="/account/about-us" />
    </div>
  </q-page>
</template>

<script setup>
import SvgIcon from 'src/components/SvgIcon.vue'
import MenuItem from 'src/components/profile/MenuItem.vue'
import { useRouter } from 'vue-router';
import { useProfileStore } from 'src/stores/profileStore';
import { computed, onMounted } from 'vue';
import { formatNumber } from 'src/utils/Format';

const profileStore = useProfileStore()
const profile = computed(() => profileStore.profile)



onMounted(async() => {
  await profileStore.fetchProfile()
  console.log(profile.value)
})
const router = useRouter()
</script>

<style scoped>

.wallet-summary {
  gap: 1rem;
}
.badge{
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  border: 1px solid rgba(40, 167, 69, 1);
  background-color: rgba(234, 250, 238, 1);
  margin-left: 1rem;
}
.badge-false{
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  border: 1px solid var(--q-negative);
  background-color: rgb(255, 219, 215);
  margin-left: 1rem;
}
.wallet-box {
  background: rgba(242, 247, 253, 1);
  border-radius: 0.5rem;
}
.menu-list {
  display: flex;
  flex-direction: column;
  margin-top: 0.5rem;
}
.custom-btn{
  background-color: transparent;
  border: none;
  outline: none;
}
</style>
