<template>
  <div @click="handleClickedNotif(id)" :class="['notification-card', { 'notification-card-read': isRead }]" >
    <!-- آیکون بالای راست -->
    <div class="icon-container flex q-mb-xs">
      <SvgIcon class="ignot-icon q-ml-xs" name="ignot" size="16" state="black" />
      <div class="typography-body-lg-medium">
      {{ title }}
      </div>
    </div>

    <!-- محتوای اصلی -->
    <div class="content full-width">
      <p class="typography-body-md-regular text-grey-darker body-text">
        {{ message }}
      </p>
      <p class="typography-caption-md-regular text-left text-timeStamp full-width timestamp">
        {{ timestamp }}
      </p>
    </div>
  </div>
  <div class="devider q-px-sm"></div>
  <notifDialogComponent
    v-model:modalValue="showDialog"
    :title="title"
    :message="message"
    :timestamp="timestamp"
    @show="onDialogShown"
/>

</template>

<script setup>
import { ref } from 'vue';
import notifDialogComponent from './notifDialogComponent.vue';
import SvgIcon from 'components/SvgIcon.vue';

const showDialog = ref(false)
const emit = defineEmits(['notifOpened'])

const props = defineProps({
  /** متن نوتیفیکیشن */
  message: {
    type: String,
    required: true
  },
  /** متن زمان (مثلا "1 ساعت پیش") */
  timestamp: {
    type: String,
    required: true
  },
  title: {
    type : String,
    required: true
  },
  isRead:{
    type: Boolean,
    required : true
  },
  id: {
    type: Number,
    required: true
   },
});

function onDialogShown() {
  if (!props.isRead) {
    emit('notifOpened', props.id)
  }
}


function handleClickedNotif(){
  showDialog.value = true
  if (!props.isRead) {
    emit('notifOpened', props.id)
  }
}


</script>

<style scoped>
.notification-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border-right: 3px solid #66BFA1; /* سبز تیره برای لبهٔ برجسته */
  padding: 0.25rem 1rem 0.25rem 1rem;
}
.notification-card.notification-card-read {
  border-right: 3px solid var(--white-light-active); /* خونده‌شده - سفید کم‌رنگ */
}

.content {
  flex: 1;
}

.body-text {
  margin: 0;
  margin-bottom: 0.2rem;
  color: #191919;
}

.timestamp {
  width: 100%;
  margin-bottom: 0;
  margin-left: 0.2rem;
  color: #656565;
}
.ignot-icon{
  padding: 0.25rem;
  background-color: var(--white-light-active);
}
.devider{
  margin-top: 0.7rem;
  margin-bottom: 0.5rem;
  border: 0.5px solid #D9D9D9;
}
</style>
