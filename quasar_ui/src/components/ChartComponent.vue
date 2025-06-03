<template>
  <div v-if="hasValidData" class="chart-container">

    <!-- filter data  -->
    <div class="time-filter-container q-mb-md q-pa-xs bg-white-light-active flex items-center justify-between">
      <div
        v-for="(item, index) in options"
        :key="index"
        :class="['time-option typography-caption-md-regular text-black', { active: modelValue === item.value }]"
        @click="modelValue = item.value"
      >
        {{ item.label }}
      </div>
    </div>

    <!-- نمودار -->
    <div class="chart-wrapper q-px-none">
      <Line ref="chartRef" :data="internalData" :options="chartOptions" />
    </div>


    <!-- فیلترهای زمانی -->
    <div  class="time-indicators">
      <div v-for="date in profitIndicators" :key="date.value" class="indicator typography-caption-md-regular flex column items-center justify-between">
        <span class="q-mb-xs" >{{date.label}}</span>
        <div :class="date.profit >= 0 ? 'text-positive': 'text-negative'" class="flex items-center text-center">{{ Math.abs(date.profit) }}٪<SvgIcon :name="date.profit >= 0 ? 'caret-up' : 'caret-down'" state="black" size="16" class="text-center"/></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
  Tooltip
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { onMounted, ref, nextTick, watch, computed } from 'vue'
import SvgIcon from './SvgIcon.vue'


const props = defineProps({
  data: Object,
  timestamps: Object,
  color:            { type: String, default:'#E7C24D' },
  profitIndicators: { type: Array, default: ()=>[] }
})

const modelValue = ref('24h')

const hasValidData = computed(() => {
  return props.data?.[modelValue.value]?.chart?.length > 0
})


watch(
  [() => props.data, () => props.timestamps,() => modelValue.value],
  async () => {
    await nextTick()
    const chart = chartRef.value?.chart
    if (!chart) return


    // اعمال گرادینت اینجا
    const ctx = chart.ctx
    const gradient = ctx.createLinearGradient(0, 0, 0, chart.height)
    gradient.addColorStop(0, `${props.color}33`)
    gradient.addColorStop(1, 'rgba(255,255,255,0)')
    chart.data.datasets[0].backgroundColor = gradient

    chart.update()
  },
  { immediate: true }
)



const chartRef = ref(null)
const options = [
  { label: '۲۴ ساعت', value: '24h' },
  { label: '۱ هفته', value: '1w' },
  { label: '۱ ماه', value: '1m' },
  { label: '۳ ماه', value: '3m' },
  { label: '۱ سال', value: '1y' }
]

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Filler, Tooltip)

const toPersianDigits = (num) => {
  const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
  return String(num).replace(/[0-9]/g, w => persianDigits[w])
}

const formatToMillions = (value) => {
  return toPersianDigits(Math.floor(value / 1000000)) + ',' +
         toPersianDigits(String(Math.floor((value % 1000000) / 1000)).padStart(3, '0')) + ',' +
         toPersianDigits(String(value % 1000).padStart(3, '0'))
}

ChartJS.register({
  id: 'dashedGridFixer',
  beforeDraw(chart, args, options) {
    if (!chart || !chart.chartArea || !chart.scales || !chart.scales.y) {
      return
    }
    const { ctx, chartArea, scales } = chart
    const yScale = scales.y

     if (!yScale || !yScale.ticks || !Array.isArray(yScale.ticks)) {
      return
    }

    ctx.save()
    ctx.beginPath()
    ctx.setLineDash(options.dash || [5, 5])
    ctx.lineWidth = options.width || 1
    ctx.strokeStyle = options.color || '#D0D0D0'

    yScale.ticks.forEach((_, index) => {
      const y = yScale.getPixelForTick(index)
      ctx.moveTo(chartArea.left, y)
      ctx.lineTo(chartArea.right, y)
    })

    ctx.stroke()
    ctx.restore()
  }
})

ChartJS.register({
  id: 'customXAxisDashedGrid',
  beforeDraw(chart) {
    if (!chart?.chartArea || !chart?.scales?.x) return
    const { ctx, scales } = chart
    const xScale = scales.x
    const y =  xScale.bottom - 30// فاصله کمی بالاتر از برچسب‌ها

    ctx.save()
    ctx.strokeStyle = '#D0D0D0'
    ctx.lineWidth = 1
    ctx.setLineDash([2, 2]) // استایل خط‌چین

    xScale.ticks.forEach((_, i) => {
      const x = xScale.getPixelForTick(i)

      // رسم ۳ خط عمودی کوچک رو به بالا
      for (let j = 0; j < 3; j++) {
        const yStart = y - j * 4 // هر خط بالاتر از قبلی
        ctx.beginPath()
        ctx.moveTo(x, yStart)
        ctx.lineTo(x, yStart - 4)
        ctx.stroke()
      }
    })

    ctx.restore()
  }
})


ChartJS.register({
  id: 'startEndVerticalLines',
  beforeDraw(chart) {
    if (!chart?.chartArea || !chart?.scales?.x) return
    const { ctx, chartArea, scales } = chart
    const xScale = scales.x
    const yBottom = chartArea.bottom + 4

    const firstX = xScale.getPixelForTick(0)
    const lastX = xScale.getPixelForTick(xScale.ticks.length - 1)

    ctx.save()
    ctx.beginPath()
    ctx.setLineDash([]) // solid
    ctx.strokeStyle = '#D0D0D0'
    ctx.lineWidth = 3
    ctx.lineCap = 'round'

    // First short vertical line (12px height)
    ctx.moveTo(firstX, yBottom)
    ctx.lineTo(firstX, yBottom - 12)

    // Last short vertical line (12px height)
    ctx.moveTo(lastX, yBottom)
    ctx.lineTo(lastX, yBottom - 12)

    ctx.stroke()
    ctx.restore()
  }
})

const internalData = computed(() => {
  // Safety checks
  if (!props.data || !props.data[modelValue.value] || !props.timestamps) {
    return {
      labels: [],
      datasets: [{
        label: '',
        data: [],
        borderColor: props.color,
        fill: true,
        tension: 0,
        borderWidth: 3,
        pointRadius: 0,
        pointHoverRadius: 4
      }]
    }
  }

  return {
    labels: props.timestamps,
    datasets: [{
      label: '',
      data: props.data[modelValue.value].chart || [],
      borderColor: props.color,
      fill: true,
      tension: 0,
      borderWidth: 3,
      pointRadius: 0,
      pointHoverRadius: 4
    }]
  }
})



const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  layout: {
    padding: { top: 10, right: 0, bottom: 10, left: 0 }
  },
  interaction: {
    mode: 'nearest',
    intersect: false,
  },
  scales: {
    x: {
      ticks: {
        font: { family: 'iranYekanWeb', size: 10, weight: '400' },
        color: '#000000',
        align: 'center',
        padding: 10,
      },
      grid: { display: false },
      border: { display: false }
    },
    y: {
      beginAtZero: false,
      ticks: {
        maxTicksLimit: 6,
        callback: (value) => formatToMillions(value),
        font: { family: 'iranYekanWeb', size: 10, weight: '400' },
        color: '#000000',
        padding: 0,
      },
      grid: { display: false },
      border: { display: false }
    }
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(12, 38, 71, 1)',
      titleColor: 'rgba(255, 255, 255, 1)',
      bodyColor: 'rgba(255, 255, 255, 1)',
      corenrRadius:8,
      padding: 8,
      displayColors: false,
      titleFont: { family: 'iranYekanWeb', size: 10, weight: 'bold',lineHeight: 1.4, },
      bodyFont: { family: 'iranYekanWeb', size: 10, },
      callbacks: {
        title: (ctx) => {
      const index = ctx[0].dataIndex
      const value = ctx[0].raw
      const time = props.timestamps?.[index] || ''
      return `${formatToMillions(value)} تومان\n${time}`
    },
    label: () => '',
      }
    },
    dashedGridFixer: {
      dash: [5, 5],
      width: 1.5,
      color: '#E6E6E6'
    },
    xAxisVerticalDashedLines: {},
    startEndVerticalLines: {}
  }
}


onMounted(async () => {
  await nextTick()

  const chart = chartRef.value?.chart
  if (!chart) return

  const ctx = chart.ctx
  const gradients = {
    '#E7C24D': [ // طلا
      'rgba(231, 194, 77, 0.2)',  // بالا
      'rgba(228, 229, 241, 0.1)'  // پایین
    ],
    '#8F8F8F': [ // نقره
      'rgba(143, 143, 143, 0.2)',
      'rgba(228, 229, 241, 0.1)'
    ],
    '#1178AE': [ // دلار
      'rgba(17, 120, 174, 0.2)',
      'rgba(228, 229, 241, 0.1)'
    ]
  }

  // پیدا کردن index دیتاست پایین‌تر
  const lowestDatasetIndex = chart.data.datasets.reduce((lowestIndex, ds, i, arr) => {
    const currentMin = Math.min(...(Array.isArray(ds.data) ? ds.data : []))

    const lowestMin = Math.min(...(Array.isArray(arr[lowestIndex].data) ? arr[lowestIndex].data : []))

    return currentMin < lowestMin ? i : lowestIndex
  }, 0)

  // اعمال گرادینت برای هر دیتاست
  chart.data.datasets.forEach((ds, i) => {
  const gradient = ctx.createLinearGradient(0, 0, 0, chart.height)

  if (i === lowestDatasetIndex) {
    const [top, bottom] = gradients[ds.borderColor] || ['rgba(0,0,0,0.2)', 'rgba(228,229,241,0.1)']
    gradient.addColorStop(0, top)
    gradient.addColorStop(1, bottom)
  } else {
    gradient.addColorStop(0, 'rgba(0,0,0,0)')
    gradient.addColorStop(1, 'rgba(0,0,0,0)')
  }

  ds.backgroundColor = gradient
})


  chart.update()
})


</script>

<style scoped>
.chart-container {
  width: 100%;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  min-height: 19.375rem; /* 310px */
}

.chart-wrapper canvas {
  width: 100% !important;
}

.price-header {
  margin-bottom: 0.9375rem; /* 15px */
  text-align: right;
}

.price-label {
  font-size: 0.875rem; /* 14px */
  color: #444;
}

.price-value {
  font-size: 1.125rem; /* 18px */
  font-weight: bold;
  color: #000;
  margin-right: 0.5rem; /* 8px */
}

.time-indicators {
  display: flex;
  justify-content: space-between;
  border-radius: 0.375rem; /* 6px */
  padding: 0.5rem; /* 8px */
  border: 1px solid var(--white-light-active);
  margin-bottom: 1rem; /* 16px */
}

.indicator {
  padding: 0.25rem; /* 4px */
  color: rgba(64, 64, 65, 1);
}

.time-filter-container {
  border-radius: 0.5rem; /* 8px */
}

.time-option {
  flex: 1;
  text-align: center;
  padding: 0.5rem; /* 8px */
  border-radius: 0.5rem; /* 8px */
  cursor: pointer;
  transition: all 0.2s ease;
}

.time-option.active {
  background-color: white;
  font-weight: 700;
}
</style>

