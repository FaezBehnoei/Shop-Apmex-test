<template>
  <q-page>
    <!-- image  -->
    <div>
      <img src="/images/invitefrineds.svg" alt="invite-friend-pic" class="full-width" />
    </div>

    <!-- content  -->
    <div class="q-px-md q-mt-sm">
      <!-- Invite Code Box -->
      <div class="flex justify-between items-center q-mb-lg">
        <!-- input box -->
        <div class="invite-box flex items-center bg-white q-py-sm q-ml-md">
          <div class="invite-content full-width">
            <label for="inviteCode" class="typography-caption-lg-regular q-mb-xs label-div">کد دعوت شما</label>
            <div class="input-wrapper">
              <input
                id="inviteCode"
                type="text"
                v-model="inviteCode"
                class="form-input-invite"
                readonly
              />

              <button class="copy-btn flex flex-center q-pl-xs" @click="copyCode">
                <SvgIcon name="copy-fill-profile" state="colored" size="24" />
              </button>
            </div>
          </div>
        </div>

        <!-- share icon -->
        <div class="icon-wrapper flex flex-center">
          <SvgIcon name="share-profile" state="balck" size="24" />
        </div>
      </div>

      <!-- Invitees List -->
      <div
        v-for="(person, index) in invitees"
        :key="person.id"
        class="invitee-card flex justify-between items-center bg-white q-pa-md q-mb-sm"
      >
        <div class="text-black typography-caption-lg-regular">{{ index + 1 }}. {{ person.name }}</div>
        <div class="text-black typography-caption-lg-regular">{{ person.date }}</div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import SvgIcon from 'src/components/SvgIcon.vue';
import { onMounted, ref } from 'vue';
import { copyToClipboard } from 'quasar';
import { getProfileInviteCode } from 'src/services/profileServices';

const inviteCode = ref(null);
const invitees = ref([]);

function copyCode() {
  copyToClipboard(inviteCode.value).then(() => {
    console.log('Copied!');
  });
}

async function getInviteCode() {
  const data = await getProfileInviteCode()
  inviteCode.value = data.invite_code
  invitees.value = data.invitees
}
onMounted(() => {
  getInviteCode()
})
</script>

<style scoped>
.invite-box {
  flex: 1;
  border-radius: 12px;
  position: relative;
  flex-direction: column;
}

.label-div {
  position: absolute;
  top: -3%;
  right: 2%;
  padding-inline: 1px;
  z-index: 999;
  background-color: white;
  margin-bottom: 0.25rem;
  color: #8A8A8A;
}

.input-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.form-input-invite {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #f2f2f2;
  border-radius: 0.5rem;
  background-color: #fff;
  font-size: 0.875rem;
  color: #000;
  font-family: inherit;
  outline: none;
}

.copy-btn {
  position: absolute;
  left: 0.25rem;
  top: 50%;
  transform: translateY(-50%);
}

.icon-wrapper {
  border-radius: 0.5rem;
  background-color: var(--orange-primary);
  height: 100%;
  padding: 0.5rem;
}

.invitee-card {
  position: relative;
  border: 1px solid #f2f2f2;
  border-radius: 8px;
}
.copy-btn{
  border: none;
  outline: none;
  background-color: transparent;
}
</style>
