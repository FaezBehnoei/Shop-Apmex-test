<template>
  <q-page class="q-px-md">
    <div class="main-container-rial flex column item-center justify-center" :class="open ? 'isOpend': ''">
      <!-- title -->
      <div class="flex items-center justify-between margin-title">
        <div class="typography-body-md-regular text-black">مبلغ واریزی خود را وارد کنید</div>
      </div>

      <!-- input -->
      <div class="flex column q-mb-md">
        <div class="flex bg-white-light-active input-div-wrapper q-mb-sm" :class="open? 'isopended': ''">
          <input v-model="amount" @input="converPriceToUnit" type="text" class="input-custom-rial full-width bg-white-light-active" placeholder="۷۰,۰۰۰,۰۰۰"/>
          <span class="rial-span">ریال</span>
        </div>
        <div class="typography-caption-lg-regular text-grey-custom">معادل {{ calculateToman() }} تومان</div>
      </div>
       <!-- quick amounts -->
      <div class="typography-body-md-regular q-mb-md">مبالغ پر تکرار</div>
      <div class="flex item-center justify-between q-gutter-x-sm q-mb-xl">
        <button @click="handleQuickAmounts(item.amount)" v-for="item in quickAmount" :key="item.id" class="quick-amount-btn typography-caption-lg-medium flex flex-center">{{ formatNumber(item.amount/1000000) }} میلیون تومان</button>
      </div>

      <!-- equivalent values -->
      <div>
        <div class="flex justify-between bg-white-light-active equivalent-item q-mb-sm">
          <span class="typography-body-md-regular text-grey-dark">{{ goldAmount }} گرم طلا</span>
        </div>
        <div class="flex justify-between bg-white-light-active equivalent-item">
          <span class="typography-body-md-regular text-grey-dark">{{ silverAmount }} گرم نقره</span>
        </div>
      </div>


      <!-- button -->
      <div class="flex flex-center">
        <ButtonComponent :loading="loading" @click="handleDepositPost" size="lg" label="واریز وجه" type="primary" class="custom-btn-deposit" />
      </div>
    </div>

  </q-page>
</template>

<script setup>
import ButtonComponent from 'src/components/ButtonComponent.vue';
import { onMounted, ref } from 'vue';
import { persianToEnglish, englishToPersian } from 'src/composable/useNumberUtils';
import { depositToWallet, getQuickNumbersWallet } from 'src/services/walletServis';
import { formatNumber } from 'src/utils/Format';
import { useRouter } from 'vue-router';

const amount = ref('')
const goldAmount = ref('.')
const silverAmount = ref('.')
const open = ref(false)
const currentPriceGold = ref(65800000)
const currentPriceSilver = ref(3580000)
const loading = ref(false)
const router = useRouter()


const quickAmount = ref([])

function converPriceToUnit(event){
  try{
    const input = persianToEnglish(event.target.value).replace(/,/g,'')
    if(input && !isNaN(Number(input))){
      const formmatedRial = Number(input).toLocaleString()
      amount.value = englishToPersian(formmatedRial)

      const finalAmountGold = Number(input) / currentPriceGold.value
      goldAmount.value = englishToPersian(finalAmountGold.toFixed(4))
      const finalAmountSilver = Number(input) / currentPriceSilver.value
      silverAmount.value = englishToPersian(finalAmountSilver.toFixed(4))
    }else if( input === ''){
      amount.value = ''
      goldAmount.value = '.'
      silverAmount.value = '.'
    }
  }catch(err){
    console.log(err)
  }
}

function calculateToman(){
    const rialInEnglish = persianToEnglish(amount.value).replace(/,/g,'')
    if(rialInEnglish && !isNaN(Number(rialInEnglish))){
      const tomanValue = Math.floor(Number(rialInEnglish) / 10)
      return englishToPersian(tomanValue.toLocaleString())
    }
    return '.'
}

async function handleDepositPost(){
  const payload = {
    amount : amount.value.replace(/,/g,'')
  }
  if(loading.value) return;
  loading.value = true
  try{
    await depositToWallet(payload)
  }finally{
    loading.value = false
    router.push('/account/wallet')
  }
}

onMounted(async() => {
 const data =  await getQuickNumbersWallet()
 quickAmount.value = data.quick_amounts
})

function handleQuickAmounts(milionAmount){
  const rial =  milionAmount * 10
  const formmated = englishToPersian(Number(rial).toLocaleString())
  amount.value = formmated

  converPriceToUnit({target : {value: formmated}})
}
</script>

<style scoped>
.main-container-rial {
  margin-top: 1rem;             /* 16px */
  padding: 1.5rem 0 4.8125rem 0; /* 24px 0px 77px 0px */
}

.main-container-rial.isOpend {
  background-color: var(--white-light-active);
  padding-right: 2rem;
  padding-left: 1rem;
  border-radius: 1rem; /* 16px */
}

.main-container-rial.isOpend > * {
  width: calc(100% - 2rem);
}

.isopended {
  background-color: white;
  border: 1px solid grey;
}

.input-div-wrapper {
  padding: 0.625rem 0.5rem; /* 10px 8px */
  position: relative;
  border-radius: 0.5rem;   /* 8px */
  min-height: 2.75rem;     /* 44px */
}

.rial-span {
  position: absolute;
  top: 50%;             /* 10px */
  left: 0.5rem;
  transform: translateY(-50%);             /* 8px */
  padding-right: 0.5rem;     /* 8px */
  border-right: 1px solid rgba(217, 217, 217, 1);
}

.input-div-wrapper:focus-within {
  background-color: var(--white-light-active);
  border: 1px solid var(--orange-primary);
}

.input-custom-rial {
  border: none;
  outline: none;
  direction: ltr;
  padding-left: 2.5rem; /* 40px */
}

.input-custom-rial:focus {
  background-color: var(--white-light-active);
}

.margin-title {
  margin-bottom: 0.75rem; /* 12px */
}

.equivalent-item {
  padding: 0.8125rem 1rem; /* 13px 16px */
  border-radius: 0.5rem;   /* 8px */
}

.quick-amount-btn {
  background-color: rgba(219, 237, 239, 1);
  color: rgba(17, 138, 146, 1);
  padding: 0.5rem;         /* 8px */
  border-radius: 0.5rem;   /* 8px */
  text-align: center;
  border: none;
  outline: none;
  flex: 1;
}

.custom-btn-deposit {
  margin-top: 4.5rem;      /* 72px */
}
</style>

