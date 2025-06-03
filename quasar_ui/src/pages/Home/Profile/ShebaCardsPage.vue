<template>
  <div class="q-px-md q-mb-md" v-for="card in bankCards" :key="card.id">
    <BankShebaCardComponent
      :sheba="card.iban"
      :bank-name="card.bank_name"
      :bank-logo="card.icon_url"
    />
  </div>

  <div class="q-px-md q-mt-xl">
    <ButtonComponent
      size="lg"
      type="stroke"
      label="افزودن شماره شبا جدید"
      @click="openShebaCardDialog"
      />
  </div>
  <DialogAddCardNumber
  v-model="showModal"
  @submit="refreshCards"/>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import BankShebaCardComponent from 'src/components/profile/BankShebaCardComponent.vue';
import ButtonComponent from 'src/components/ButtonComponent.vue';
import DialogAddCardNumber from 'src/components/profile/DialogAddCardNumber.vue';
import { getProfileSHebaBankCards } from 'src/services/profileServices';

const showModal = ref(false)
function openShebaCardDialog(){
  showModal.value = true
}
const bankCards = ref([])
onMounted(async() => {
  const data = await getProfileSHebaBankCards()
  bankCards.value = data
})
async function refreshCards(){
  const data = await getProfileSHebaBankCards()
  bankCards.value = data
}
</script>
