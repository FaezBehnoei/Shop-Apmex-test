<template>
  <q-page v-if="product" class="product-detail-page flex">

    <!-- Image Preview -->
    <!-- Carosel  -->
      <div class="flex flex-center full-width carousel-background">
        <ProductIMGcarousel v-if="product"   :slides="normalizeImages(product.images, product.title)"
          :auto-play="true" :auto-play-interval="2000" />
      </div>

    <div class="gold-receipt-page full-width">
      <div>
        <!-- Title and Price -->
      <div class="text-section flex items-center justify-between q-mb-md">
        <div class="text-right typography-body-md-bold text-black q-mb-xs">{{ product.title }}</div>
        <div class="text-orange typography-body-lg-bold q-mb-sm">{{ formatNumber(product.price) }} تومان</div>
      </div>

      <!-- Info Box -->
      <div class="info-box flex justify-evenly q-py-sm q-px-md q-mb-md">
        <div class="text-center flex column justify-between q-gutter-y-md">
          <div class="typography-caption-lg-regular text-color-weight">وزن</div>
          <div class="typography-caption-lg-bold text-black">{{ product.weight }}</div>
        </div>
        <div class="devider"></div>
        <div class="text-center flex column justify-between q-gutter-y-md">
          <div class="typography-caption-lg-regular text-color-weight">عیار</div>
          <div class="typography-caption-lg-bold text-black">{{ product.ayar }}</div>
        </div>
      </div>

      <!-- Product description -->
        <div class="product-description text-right">
          <div class="description-title text-right typography-body-md-medium q-mb-xs">توضیحات</div>
          <p class="description-text text-white-darker typography-caption-lg-regular q-mb-sm">
            {{ product.description }}
          </p>
        </div>
      </div>
      <!-- Quantity + Button -->
      <div class="action-row flex justify-between items-center q-px-md q-mb-xl">
        <div class="btn-wrapper">
          <ButtonComponent
          label="افزودن به سبد خرید"
          type="primary"
          size="lg"
          class=""
          @click="addToCart"
        />
        </div>
        <div class="qty-box flex row items-center">
          <button class="plus-icon flex flex-center" @click="increaseQty" >
            <SvgIcon name="plus-shop" state="black" size="16"  />
          </button>
          <div class="qty-text typography-body-md-bold">{{ quantity }}</div>
          <button class="minus-icon flex flex-center" @click="decreaseQty" :disable="quantity === 1" >
            <SvgIcon name="minus-shop" state="black" size="16" />
          </button>
        </div>


      </div>

    </div>

  </q-page>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import ButtonComponent from 'src/components/ButtonComponent.vue';
import { formatNumber } from 'src/utils/Format';
import { useShopStore } from 'src/stores/ShopStore';
import { usePageTitle } from 'src/composable/usePageTitle';
import ProductIMGcarousel from 'src/components/ProductIMGcarousel.vue';
import SvgIcon from 'src/components/SvgIcon.vue';

const route = useRoute();
const shopStore = useShopStore()

const quantity = ref(1);
const product = ref({});
function normalizeImages(imageInput, altText = '') {
  if (!imageInput) return []

  if (Array.isArray(imageInput)) {
    return imageInput.map(img => ({ image: img, alt: altText }))
  }

  return [{ image: imageInput, alt: altText }]
}

const increaseQty = () => {
  quantity.value++;
};
const decreaseQty = () => {
  if (quantity.value > 1) quantity.value--;
};

const addToCart = () => {
  console.log('Add to cart:', product.value.id, quantity.value);
};

watch(
  () => product.value?.title,
  (title) => {
    if (title) usePageTitle(title)
  },
  {immediate: true}
)
watch(() => route.params.id,
async(id) => {
  if (id) {
    await shopStore.fetchShopProductsById(id)
    product.value = shopStore.selectedProduct
  }
},
  {immediate: true}
)



</script>

<style scoped>
.carousel-background{
  background-color: #F7F7F7;
  padding-bottom: 2rem;
}
.gold-receipt-page {
  padding: 1.5rem 1rem;
  background-color: white;
  width: 100%;
  border-top-left-radius: 2.5rem;  /* 40px */
  border-top-right-radius: 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-top: -2rem;
  flex-grow: 1;
}
.product-detail-page {
  background-color: #fff;
}

.header {
  margin-top: 0.75rem;
}

.product-image-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.product-img {
  width: 180px;
  height: auto;
  object-fit: contain;
}

.dot-indicator .dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background-color: #d3d3d3;
  margin-inline: 4px;
}
.dot-indicator .dot.active {
  background-color: var(--orange-primary);
}

.info-box {
  background-color: #F7F7F7;
  border-radius: 16px;
}

.description-box {
  line-height: 1.8;
}

.qty-box {
  background-color: #f5f5f5;
  padding: 0.75rem 0.5rem;
  border-radius: 0.5rem;
  gap: 1rem;
}

.qty-text {
  padding: 0 0.75rem;
}

.devider{
  height: 4em;
  width: 2px;
  background-color: #CFCFCF;
}
.text-color-weight{
  color: rgba(89, 89, 89, 1);
}
.description-text {
  margin-bottom: 0;
  text-align: justify;
}
.plus-icon{
  padding: 0.25rem;
  background-color: var(--orange-primary);
  color: rgba(233, 237, 245, 1);
  border: none;
  border-radius: 2px;
}
.minus-icon{
  padding: 0.25rem;
  background-color: rgba(255, 242, 235, 1);
  color: var(--orange-primary);
  border: none;
  border-radius: 2px;
}
.action-row{
  display: flex;
  max-width: 100%;
  gap: 1rem;
}
.btn-wrapper{
  flex-grow: 1;
}
</style>
