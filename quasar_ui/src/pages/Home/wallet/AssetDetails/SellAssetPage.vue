<template>
  <q-page class="q-px-md q-pt-sm q-mt-md">
    <div class="main-container flex column item-center justify-center">

      <!-- Balance -->
      <div class="flex items-center justify-between ">
        <div class="typography-body-md-regular text-black">موجودی شما:</div>
        <div>
          <span class="typography-body-md-regular text-black q-ml-xs">۱۶۵,۵۵۷,۰۰۰</span>
          <span class="typography-caption-md-regular text-grey-custom">ریال</span>
        </div>
      </div>

      <!-- Input for gold amount -->
      <div class="flex column ">
        <div class="flex bg-white-light-active input-div-wrapper">
          <input @input="convertUnitToPrice" v-model="Amount" type="text" class="input-custom full-width bg-white-light-active" />
          <span class="unit-span">گرم</span>
        </div>
      </div>

      <!-- Price display -->
      <div class="flex column q-mb-xs">
        <div class="flex bg-white-light-active input-div-wrapper q-mb-sm">
          <input @input="convertRialToAmount" v-model="rialAmount" type="text" class="input-custom full-width bg-white-light-active" />
          <div class="flex flex-center full-height">
            <span class="unit-span flex flex-center">ریال</span>
          </div>
        </div>
        <!-- Toman equivalent -->
        <div class="typography-caption-lg-regular text-grey-custom text-right">معادل {{ calculateToman() }} تومان</div>
      </div>

      <!-- Button -->
      <div class="flex flex-center">
        <ButtonComponent label="فروش" size="lg" />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import ButtonComponent from 'src/components/ButtonComponent.vue';
import { englishToPersian, persianToEnglish } from 'src/composable/useNumberUtils';
import { ref } from 'vue';

const Amount = ref('');
const rialAmount = ref('');
const currentPrice = ref(64340000);

function convertUnitToPrice(event) {
  try {
    const engAmount = persianToEnglish(event.target.value).replace(/,/g, '');

    if (engAmount && !isNaN(Number(engAmount))) {
      const finalPriceInEnglish = Number(engAmount) * currentPrice.value;
      rialAmount.value = englishToPersian(finalPriceInEnglish.toLocaleString());
    } else if (engAmount === '') {
      rialAmount.value = '';
    }
  } catch (error) {
    console.error('Error in convertUnitToPrice:', error);
  }
}

function convertRialToAmount(event) {
  try {
    const input = persianToEnglish(event.target.value).replace(/,/g, '');

    if (input && !isNaN(Number(input))) {
      const formattedRial = Number(input).toLocaleString();
      rialAmount.value = englishToPersian(formattedRial);

      const finalAmount = Number(input) / currentPrice.value;
      Amount.value = englishToPersian(finalAmount.toFixed(4));
    } else if (input === '') {
      Amount.value = '';
      rialAmount.value = '';
    }
  } catch (error) {
    console.error('Error in convertRialToAmount:', error);
  }
}

function calculateToman() {
  try {
    const rialInEnglish = persianToEnglish(rialAmount.value).replace(/,/g, '');
    if (rialInEnglish && !isNaN(Number(rialInEnglish))) {
      const tomanValue = Number(rialInEnglish) / 10;
      return englishToPersian(tomanValue.toLocaleString());
    }
    return '۰';
  } catch (error) {
    console.error('Error in calculateToman:', error);
    return '۰';
  }
}
</script>

<style scoped>
.main-container {
  gap: 1.5rem; /* بدون تغییر چون از قبل rem بود */
  padding: 1.5rem 1rem;
}

.input-div-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 0.5rem; /* 8px */
  min-height: 2.75rem; /* 44px */
  border: 1px solid rgba(217, 217, 217, 0.5);
}

.unit-span {
  position: absolute;
  top: 50%; /* 10px */
  transform: translateY(-50%);
  left: 0.5rem; /* 8px */
  padding-right: 0.5rem; /* 8px */
  border-right: 1px solid rgba(217, 217, 217, 1);
}

.input-div-wrapper:focus-within {
  background-color: var(--white-light-active);
  border: 1px solid var(--orange-primary);
}

.input-custom {
  border: none;
  outline: none;
  direction: ltr;
  border-radius: 0.5rem;
  padding-left: 2.5rem; /* 40px */
  font-size: 1rem; /* 16px */
}

.input-custom:focus {
  background-color: var(--white-light-active);
}

.price-display {
  background-color: rgba(240, 240, 240, 1);
  padding: 0.75rem 1rem; /* 12px 16px */
  border-radius: 0.5rem; /* 8px */
}
</style>
