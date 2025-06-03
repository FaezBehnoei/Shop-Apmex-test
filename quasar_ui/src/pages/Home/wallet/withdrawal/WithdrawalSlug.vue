<template>
  <q-page class="q-px-md">
    <div class="main-container-rial flex column item-center justify-center" :class="open ? 'isOpend' : ''">
      <!-- title  -->
      <div class="flex items-center justify-between margin-title">
        <div class="typography-body-md-regular text-black">موجودی قابل برداشت:</div>
        <div>
          <span class="typography-body-md-regular text-blue-custom q-ml-xs">۱۶۵,۵۵۷,۰۰۰</span>
          <span class="typography-caption-md-regular text-white-dark">گرم</span>
        </div>
      </div>

      <!-- input section -->
      <div class="flex column q-mb-md">
        <!-- input: gold -->
        <div v-if="!isRial" class="flex bg-white-light-active input-div-wrapper q-mb-md" :class="open ? 'isopended' : ''" >
          <input @input="convertUnitToPrice" v-model="amountGold" type="text" class="input-custom-rial full-width bg-white-light-active" :class="open ? 'isopended' : ''"/>
          <span class="rial-span">گرم</span>
        </div>

        <!-- input: rial -->
        <div class="flex bg-white-light-active input-div-wrapper q-mt-sm q-mb-sm" :class="open ? 'isopended' : ''">
          <input @input="convertRialToAmount" v-model="amount" type="text" class="input-custom-rial full-width bg-white-light-active" :class="open ? 'isopended' : ''"/>
          <span class="rial-span">ریال</span>
        </div>

        <!-- Toman -->
        <div class="typography-caption-lg-regular text-grey-custom">معادل {{ calculateToman() }} تومان</div>
      </div>

      <!-- title -->
      <div class="typography-body-md-regular q-mb-md">شماره حساب مقصد</div>

      <!-- Shaba -->
      <div class="q-mb-lg">
        <ShabaAccounts v-model="selectedShaba" />
      </div>

      <!-- button -->
      <div class="flex flex-center">
        <ButtonComponent @click="handleOpenDialog" size="lg" label="برداشت" type="primary" class="custom-btn-withdraw" />
      </div>
    </div>

    <RecieptDialog v-model:modalValue="open" :rialBalance="calculateToman()" :shebaNumber="selectedShaba" :assetSlug="slug"/>
  </q-page>
</template>

<script setup>
import { computed, ref } from 'vue'
import ShabaAccounts from 'src/components/ShabaAccounts.vue'
import ButtonComponent from 'src/components/ButtonComponent.vue'
import RecieptDialog from 'src/components/RecieptDialog.vue'
import { englishToPersian, persianToEnglish } from 'src/composable/useNumberUtils'
import { useRoute } from 'vue-router'

const route = useRoute()
const slug = route.params.slug

const amount = ref('')
const amountGold = ref('')
const open = ref(false)
const currentPrice = ref(64340000) // قیمت هر گرم طلا
const selectedShaba = ref('')
const isRial = computed(() => route.params.slug === 'rial')
console.log(isRial.value)

function convertUnitToPrice(event) {
  try {
    const engAmount = persianToEnglish(event.target.value).replace(/,/g, '')
    if (engAmount && !isNaN(Number(engAmount))) {
      const finalPriceInEnglish = Number(engAmount) * currentPrice.value
      amount.value = englishToPersian(finalPriceInEnglish.toLocaleString())
    } else if (engAmount === '') {
      amount.value = ''
    }
  } catch (error) {
    console.error('Error in convertUnitToPrice:', error)
  }
}

function convertRialToAmount(event) {
  try {
    const input = persianToEnglish(event.target.value).replace(/,/g, '')
    if (input && !isNaN(Number(input))) {
      const formattedRial = Number(input).toLocaleString()
      amount.value = englishToPersian(formattedRial)

      const finalAmount = Number(input) / currentPrice.value
      amountGold.value = englishToPersian(finalAmount.toFixed(4))
    } else if (input === '') {
      amount.value = ''
      amountGold.value = ''
    }
  } catch (error) {
    console.error('Error in convertRialToAmount:', error)
  }
}

function calculateToman() {
  try {
    const rialInEnglish = persianToEnglish(amount.value).replace(/,/g, '')
    if (rialInEnglish && !isNaN(Number(rialInEnglish))) {
      const tomanValue = Math.floor(Number(rialInEnglish) / 10)
      return englishToPersian(tomanValue.toLocaleString())
    }
    return '۰'
  } catch (error) {
    console.error('Error in calculateToman:', error)
    return '۰'
  }
}

function handleOpenDialog(){
  if(selectedShaba.value && amount.value){
    open.value = true
  }
}
</script>

<style scoped>
.main-container-rial {
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
  border-radius: 0.5rem; /* 8px */
  min-height: 2.75rem;   /* 44px */
}

.rial-span {
  position: absolute;
  top: 0.625rem;       /* 10px */
  left: 0.5rem;        /* 8px */
  padding-right: 0.5rem; /* 8px */
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
  margin-bottom: 1.5rem; /* 24px */
}

.custom-btn-withdraw {
  padding: 0.9375rem 9.5rem !important; /* 15px 152px */
  font-weight: 700;
  font-size: 0.75rem;    /* 12px */
  line-height: 1.125rem; /* 18px */
  letter-spacing: 0%;
  max-width: fit-content;
}
</style>
