<template>
  <div class="delivery-page">

    <!-- Required Documents Section -->
    <div v-if="isInPerson" class="documents-section q-mb-lg">
      <div class="section-title typography-body-md-bold text-black q-mb-xs">مدارک مورد نیاز</div>
      <ul class="requirements-list q-pr-sm">
        <li class="requirement-item typography-caption-lg-regular text-white-dark-hover flex q-mb-sm">
          <span class="bullet">•</span>
          <span> کارت ملی</span>
        </li>
        <li class="requirement-item typography-caption-lg-regular text-white-dark-hover flex q-mb-sm">
          <span class="bullet ">•</span>
          فاکتورخرید
        </li>
        <li class="requirement-item typography-caption-lg-regular text-white-dark-hover flex q-mb-lg">
          <span class="bullet">•</span>
          طلا با خود شخص داده می شود
        </li>
      </ul>

    </div>
    <div v-if="isInPerson" class="divider q-my-md"></div>

    <!-- Branch Selection Section -->
    <div v-if="isInPerson" class="branch-section q-mt-lg q-pt-xs q-mb-lg">
      <div class="section-title typography-body-md-bold text-black q-mb-sm">یکی از شعبات زیر را انتخاب کنید</div>

      <!-- Branch Options -->
      <div class="branch-options">

        <!-- Option  -->
        <div v-for="address in addresses" :key="address.id" class="branch-option bg-white-light-hover q-mb-sm flex justify-between items-center">
          <div class="option-content flex">
          <div
            class="check-wrapper"
            :class="{ selected: selectedBranch === address.id }"
            @click="selectedBranch = address.id"
          >
            <SvgIcon v-if="selectedBranch === address.id" name="check" state="black" size="16" />
          </div>
            <div class="branch-name typography-caption-lg-regular text-white-darker">
              {{ address.address }}
            </div>
          </div>
          <div class="q-pr-sm" @click="handleClickedLocation(address)" >
              <SvgIcon name="location" state="orange" size="20" />
            </div>
        </div>
      </div>
    </div>

    <div v-if="isInPerson" class="divider q-my-md"></div>


    <!-- Date & Time Selection Section -->
    <div class="date-time-section q-pt-sm q-mb-lg">
      <div class="section-title typography-body-md-bold text-black q-mb-md">تاریخ تحویل خود را انتخاب کنید</div>

      <!-- Date Selection -->
      <div class="date-selection-container q-mb-md">
        <div
          v-for="dateObj in dates"
          :key="dateObj.id"
          class="date-column"
          :class="{ selected: selectedDateId === dateObj.id }"
        >
          <div class="date-header-with-name q-mb-md" :class="{ selected: selectedDateId === dateObj.id }">
            <div class="date-header typography-subtitle-bold text-center">{{ dateObj.date }}</div>
            <div class="day-name typography-caption-lg-regular text-center">{{ dateObj.day }}</div>
          </div>

          <div class="time-slots">
            <div
              v-for="slot in dateObj.slots"
              :key="slot"
              class="time-slot typography-body-sm-regular text-center"
              :class="{ selected: selectedDateId === dateObj.id && selectedTime === slot }"
              @click="() => {
                selectedDateId = dateObj.id
                selectedTime = slot
                selectedDate = dateObj.date
              }"
            >
              {{ slot }}
            </div>
          </div>
        </div>
      </div>

    </div>

    <div v-if="isPost" class="divider q-my-md"></div>

    <!-- address by Post  -->
     <div v-if="isPost" class="branch-section q-mt-lg q-pt-xs q-mb-lg">
      <div class="section-title typography-body-md-bold text-black q-mb-sm">آدرس محل سکونت خود را انتخاب کنید</div>

      <!-- Branch Options -->
      <div class="branch-options">

        <!-- Option  -->
        <div v-for="address in userAddresses" :key="address.id" class="branch-option bg-white-light-hover q-mb-sm flex justify-between items-center" :class="{ selected : selectedBranch === address.id }">
          <div class="option-content flex">
          <div
            class="check-wrapper"
            :class="{ selected: selectedBranch === address.id }"
            @click="selectedBranch = address.id"
          >
            <SvgIcon v-if="selectedBranch === address.id" name="check" state="black" size="16" />
          </div>
            <div class="branch-name typography-caption-lg-regular text-white-darker">
              {{ address.address }}
            </div>
          </div>
          <div class="q-pr-sm" >

              <SvgIcon name="round-edit" state="black" size="16" class="q-pl-xs" />
              <SvgIcon v-if="selectedBranch !== address.id" name="trash" state="black" size="16" />
              <SvgIcon v-else name="trash" state="red" size="16" />
            </div>
        </div>
      </div>
      <!-- new address  -->
       <div class="download-section flex justify-start q-mt-md q-px-sm">
          <button @click="handleNewAddresDialog" flat class="download-btn text-primary">
            <SvgIcon name="plus-blue" state="black" size="24" />
            <span class="text-primary q-mr-xs typography-caption-lg-regular">ثبت ادرس جدید</span>
          </button>
        </div>
    </div>

    <!-- Purchase Button -->
    <div class="purchase-button-container">
      <ButtonComponent @click="handlePurchase" size="lg" :label="btnLabel" type="primary" class="q-mt-sm full-width" />
    </div>
  </div>
  <FinalMapDialog v-model:modal-value="openDialog"  :address="selectedAddress" />
  <FinalResponseDeliveryDialog v-model:modal-value="openDialogFinal" :title="title" :body-text="finalDeliveryText"/>
  <NewAddressDialog v-model:model-value="openNewAddress"/>
</template>

<script setup>
import {  onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import SvgIcon from 'src/components/SvgIcon.vue';
import ButtonComponent from 'src/components/ButtonComponent.vue';
import FinalMapDialog from 'src/components/Delivery/FinalMapDialog.vue';
import FinalResponseDeliveryDialog from 'src/components/Delivery/finalResponseDeliveryDialog.vue';
import NewAddressDialog from 'src/components/profile/NewAddressDialog.vue';
import { getAddressAndTimeStampWallet, confirmPickedUpProductWallet } from 'src/services/walletServis';
import { useQuasar } from 'quasar';
import { usePageTitle } from 'src/composable/usePageTitle';

const route = useRoute()
const $q = useQuasar()

const isInPerson = ref(false)
const isPost = ref(false)
const btnLabel = ref('خرید')

const addresses = ref([])

const userAddresses = ref([])
const selectedAddress = ref(null)
const openDialog = ref(false)
const openDialogFinal = ref(false)
const openNewAddress = ref(false)
const title = ref('درخواست تحویل طلا')

const selectedBranch = ref(null);
const dates = ref([])

const deliveryDay = ref({
  day : '',
  date: "",
  time: ""
})
const finalDeliveryText = ref(`رزرو در روز ${deliveryDay.value.day} ${deliveryDay.value.date}  در ساعت ${deliveryDay.value.time} توسط شما انجام شد. لطفا در همان روز و ساعت در محل تحویل همراه با مدارک حضور داشته باشید.`)

const selectedDate = ref(null)
const selectedDateId = ref(null)       // e.g. 2
const selectedTime = ref(null)         // e.g. '۱۲:۰۰ - ۱۴:۰۰'

function handleClickedLocation(address){
  openDialog.value = !openDialog.value
  selectedAddress.value = address
}



async function handlePurchase(){
  if (!selectedBranch.value) {
    $q.notify({
      message: 'لطفا یک شعبه را انتخاب کنید.',
      position: 'top'
    });
    return; // جلو ارسال درخواست رو بگیر
  }
  if (!selectedDateId.value || !selectedTime.value) {
      $q.notify({
      message: 'لطفا زمان مورد نظر را انتخاب کنید',
      position: 'top'
    });
      return; // ارسال نشود
  }

  // برای روش پستی هم میتونی چک کنی که آدرس انتخاب شده باشه
  if (isPost.value && !selectedBranch.value) {
    $q.notify({
      message: 'لطفا آدرس محل سکونت را انتخاب کنید.',
      position: 'top'
    });
    return;
  }

  const pickedUpData = {
    address_id : selectedBranch.value,
    date : selectedDate.value,
    slot : selectedTime.value
  }
 const response =  await confirmPickedUpProductWallet(pickedUpData)
 deliveryDay.value = {
  day : response.weekday,
  date: response.date,
  time : response.time
 }
  if (isInPerson.value) {
    finalDeliveryText.value = `رزرو در روز ${response.weekday} ${response.date}  در ساعت ${response.time} توسط شما انجام شد. لطفا در همان روز و ساعت در محل تحویل همراه با مدارک حضور داشته باشید.`
  }

  if (isPost.value) {
    finalDeliveryText.value = `درخواست شما در روز ${response.weekday} ${response.date} ساعت ${response.time} توسط پیک به شما تحویل داده خواهد شد.`
  }
 openDialogFinal.value = true
}
function handleNewAddresDialog(){
  openNewAddress.value = true
}

onMounted(async () => {
  const method = route.query.method
  let title = ''

  if (method === 'inPerson') {
    isInPerson.value = true
    btnLabel.value = 'خرید'
    title = 'تحویل فیزیکی'
    usePageTitle(title)

    try {
      const data = await getAddressAndTimeStampWallet('inPerson')
      dates.value = data.dates
      addresses.value = data.addresses
    } catch (error) {
      console.log(error)
    }
  }

  if (method === 'byPost') {
    isPost.value = true
    btnLabel.value = 'درخواست رزرو'
    title = 'تحویل با پیک'
    usePageTitle(title)

    try {
      const data = await getAddressAndTimeStampWallet('byPost')
      dates.value = data.dates
      userAddresses.value = data.addresses
    } catch (error) {
      console.log(error)
    }
  }
})


</script>

<style scoped>
.delivery-page {
  padding: 1rem;
}

.page-header {
  margin-bottom: 1.5rem;
}

.documents-section {
  margin-bottom: 1.5rem;
}

.bullet {
  color: var(--orange-primary);
  width: 0.25rem;         /* 4px */
  height: 0.25rem;        /* 4px */
  margin-left: 0.25rem;   /* 4px */
}

.divider {
  height: 0.0625rem;      /* 1px */
  background-color: rgba(217, 217, 217, 1);
  margin: 1rem 0;
}

.branch-option {
  padding: 1.5rem 0.5rem;
  border-radius: 0.5rem;
  border: 1px solid var(--white-light-active);
}

.branch-option.selected {
  background-color: rgba(255, 239, 229, 1);
  border: 1px solid var(--orange-primary);
}

.option-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1 1 0;
  min-width: 0;
}

.branch-name {
  flex: 1 1 0;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.radio-circle {
  width: 1.125rem;         /* 18px */
  height: 1.125rem;        /* 18px */
  border-radius: 0.25rem;  /* 4px */
  margin-left: 0.25rem;    /* 4px */
  border: 1px solid #E5E5E5;
}

.radio-selected {
  color: #FF7F33;
}

.date-selection-container {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
  max-width: 100%;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.date-column {
  flex: 0 0 auto;
  border: 1px solid #E5E5E5;
  border-radius: 1.25rem 1.25rem 1.5rem 1.5rem; /* 20px 20px 24px 24px */
  padding: 0.625rem;        /* 10px */
  scroll-snap-align: start;
}

.date-column.selected {
  border: 1px solid rgba(72, 199, 142, 0.5);
}

.time-slot {
  padding: 0.5625rem 0.75rem;    /* 9px 12px */
  border-radius: 0.75rem;        /* 12px */
  margin-bottom: 0.875rem;       /* 14px */
  font-weight: 700;
  font-size: 0.875rem;           /* 14px */
  line-height: 1.375rem;         /* 22px */
  letter-spacing: 0%;
  background-color: var(--white-light-hover);
}

.time-slot.selected {
  background-color: rgba(72, 199, 142, 1);
  color: white;
}

.requirements-list {
  list-style-type: none;
}

.check-wrapper {
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem; /* 4px */
  background-color: white;
  border: 1px solid var(--white-normal-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.check-wrapper.selected {
  background-color: var(--orange-primary);
  border-color: var(--orange-primary);
}

.date-header-with-name {
  padding: 0.625rem 0.875rem; /* 10px 14px */
}

.date-header-with-name.selected {
  background-color: rgba(230, 244, 240, 1);
  border: 1px solid rgba(102, 191, 161, 1);
  border-radius: 1.125rem;      /* 18px */
  padding: 0.625rem 0.875rem;   /* 10px 14px */
}
.download-btn {
  outline: none;
  border: none;
  background-color: transparent;
  display: flex;
  align-items: center;
  color: rgba(45, 156, 219, 1);
}

</style>

