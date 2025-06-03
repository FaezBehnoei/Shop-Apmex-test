<template>
  <div class="chart-container">
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
      <!-- Tooltip داخل همین container -->
      <div ref="tooltipRef" class="custom-tooltip" v-show="showTooltip">
        <div class="tooltip-value">{{ tooltipData.value }}</div>
        <div class="tooltip-time">{{ tooltipData.time }}</div>
      </div>
    </div>

    <!-- فیلترهای زمانی -->
    <div class="time-indicators q-mx-lg">
      <div v-for="date in profitIndicators" :key="date.value" class="indicator typography-caption-md-regular flex items-center justify-between">
       <div class="profit-indicator-div q-ml-xs"
       :style="{ backgroundColor: indicatorColors[date.value] || '#ccc' }"
       ></div>
        <span >{{date.label}}</span>
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
import { ref, nextTick, watch, computed, onBeforeUnmount, reactive } from 'vue'

const indicatorColors = {
  gold: 'rgba(231, 194, 77, 1)',
  coin: 'rgba(255, 159, 102, 1)',
  silver: 'rgba(143, 143, 143, 1)',
  usd: 'rgba(102, 191, 161, 1)'
}

const props = defineProps({
  data: { type: Object, default: () => ({}) },
  timestamps: { type: Array, default: () => [] },
  color: { type: String, default: '#E7C24D' },
  profitIndicators: { type: Array, default: () => [] }
})

const modelValue = ref('24h')
const chartRef = ref(null)
const tooltipRef = ref(null)
const showTooltip = ref(false)
const tooltipData = reactive({
  value: '',
  time: '',
  x: 0,
  y: 0
})

// پاک کردن tooltip قبل از destroy شدن کامپوننت
onBeforeUnmount(() => {
  showTooltip.value = false
  // پاک کردن هر tooltip که ممکنه در DOM باشه
  const existingTooltip = document.getElementById('chartjs-tooltip')
  if (existingTooltip) {
    existingTooltip.remove()
  }
})

watch(
  [() => props.data, () => props.timestamps, () => modelValue.value],
  async () => {
    await nextTick()
    const chart = chartRef.value?.chart
    if (!chart) return

    const ctx = chart.ctx
    const rawData = props.data?.[modelValue.value] || {}

    if (Object.keys(rawData).length === 0) return

    chart.data.labels = props.timestamps || []

    const allValues = Object.values(rawData).flat()
    if (allValues.length === 0) return
    const globalMin = Math.min(...allValues)

    chart.data.datasets = Object.entries(rawData).map(([key, values]) => {
      const color = indicatorColors[key]
      const gradient = ctx.createLinearGradient(0, 0, 0, chart.height)

      if (values && Array.isArray(values) && Math.min(...values) === globalMin) {
        gradient.addColorStop(0, color.replace('1)', '0.9)'))
        gradient.addColorStop(1, 'rgba(228, 229, 241, 0.05)')
      } else {
        gradient.addColorStop(0, 'rgba(0,0,0,0)')
        gradient.addColorStop(1, 'rgba(0,0,0,0)')
      }

      return {
        label: key,
        data: values,
        borderColor: color,
        backgroundColor: gradient,
        fill: true,
        tension: 0.4,
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 4,
        pointBorderWidth: 0,
        pointHoverBorderWidth: 0,
        pointBackgroundColor: 'rgba(12, 38, 71, 1)',
        pointHoverBackgroundColor: 'rgba(12, 38, 71, 1)',
      }
    })

    chart.update('none')
  },
  { immediate: true }
)

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

// کاستوم tooltip که مشکل ساز نباشه
const customTooltipHandler = (context) => {
  const tooltipModel = context.tooltip

  if (tooltipModel.opacity === 0) {
    showTooltip.value = false
    return
  }

  if (tooltipModel.body && tooltipModel.dataPoints?.length > 0) {
    const dataIndex = tooltipModel.dataPoints[0].dataIndex
    const value = tooltipModel.dataPoints[0].raw
    const time = props.timestamps?.[dataIndex] || ''

    tooltipData.value = `${formatToMillions(value)} تومان`
    tooltipData.time = time

    tooltipData.x = Math.max(tooltipModel.caretX - 60, 10)
    tooltipData.y = Math.max(tooltipModel.caretY - 25, 10) // جلوگیری از رفتن بالای container

    showTooltip.value = true
  }
}

// Plugin های بهینه شده
ChartJS.register({
  id: 'dashedGridFixer',
  beforeDraw(chart, args, options) {
    const { ctx, chartArea, scales } = chart
    const yScale = scales.y

    if (!ctx || !chartArea || !yScale) return
    ctx.save()
    ctx.beginPath()
    ctx.setLineDash(options.dash || [5, 5])
    ctx.lineWidth = options.width || 1
    ctx.strokeStyle = options.color || '#D0D0D0'

    yScale.ticks?.forEach((_, index) => {
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
    const { ctx, scales } = chart
    const xScale = scales.x
    if (!ctx || !xScale) return
    const y = xScale.bottom - 30

    ctx.save()
    ctx.strokeStyle = '#D0D0D0'
    ctx.lineWidth = 1
    ctx.setLineDash([2, 2])

    xScale.ticks?.forEach((_, i) => {
      const x = xScale.getPixelForTick(i)

      for (let j = 0; j < 3; j++) {
        const yStart = y - j * 4
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
    const { ctx, chartArea, scales } = chart
    const xScale = scales.x
    const yBottom = chartArea.bottom + 4

    if (!xScale?.ticks || !xScale?.getPixelForTick || xScale.ticks.length === 0) return

    const firstX = xScale.getPixelForTick(0)
    const tickCount = xScale.ticks?.length || 0
    const lastX = tickCount > 0 ? xScale.getPixelForTick(tickCount - 1) : null

    if (firstX !== null && lastX !== null) {
      ctx.save()
      ctx.beginPath()
      ctx.setLineDash([])
      ctx.strokeStyle = '#D0D0D0'
      ctx.lineWidth = 3
      ctx.lineCap = 'round'

      ctx.moveTo(firstX, yBottom)
      ctx.lineTo(firstX, yBottom - 12)

      ctx.moveTo(lastX, yBottom)
      ctx.lineTo(lastX, yBottom - 12)

      ctx.stroke()
      ctx.restore()
    }
  }
})

const internalData = computed(() => {
  const rawData = props.data[modelValue.value] || {}
  const seriesColors = {
    gold: 'rgba(231, 194, 77, 1)',
    coin: 'rgba(255, 159, 102, 1)',
    silver: 'rgba(143, 143, 143, 1)',
    usd: 'rgba(102, 191, 161, 1)'
  }

  return {
    labels: props.timestamps,
    datasets: Object.entries(rawData).map(([key, values]) => ({
      label: key,
      data: values,
      borderColor: seriesColors[key],
      backgroundColor: `${seriesColors[key]}33`,
      fill: true,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointBorderWidth: 0,
      pointHoverBorderWidth: 0,
      pointBackgroundColor: 'rgba(12, 38, 71, 1)',
      pointHoverBackgroundColor: 'rgba(12, 38, 71, 1)',
    }))
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
      enabled: false,
      external: customTooltipHandler
    },
    dashedGridFixer: {
      dash: [5, 5],
      width: 1.5,
      color: '#E6E6E6'
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  min-height: 18.375rem;
  max-height: 22rem;
}

.chart-wrapper canvas {
  width: 100% !important;
}

.time-indicators {
  display: flex;
  justify-content: space-between;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}

.indicator {
  padding: 0.25rem;
  color: rgba(64, 64, 65, 1);
}

.time-filter-container {
  border-radius: 0.5rem;
}

.time-option {
  flex: 1;
  text-align: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.time-option.active {
  background-color: white;
  font-weight: 700;
}

.profit-indicator-div {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 3px;
  background-color: red;
}

.custom-tooltip {
  position: absolute;
  background-color: rgba(12, 38, 71, 1);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-family: 'iranYekanWeb';
  text-align: right;
  pointer-events: none;
  z-index: 1000;
  left: v-bind('tooltipData.x + "px"');
  top: v-bind('tooltipData.y + "px"');
  transform: translateX(-50%);
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 100px;
  max-width: 200px;
}

.tooltip-value {
  font-size: 0.625rem;
  font-weight: 400;
  line-height: 0.875rem;
  margin-bottom: 0.25rem;
}

.tooltip-time {
  font-size: 0.625rem;
  font-weight: 400;
  line-height: 0.875rem;
}
</style>
