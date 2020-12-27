<template>
<div>
  <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">
    <span>Price chart</span>
    <span v-if="start !== '' && end !== ''" class="font-normal text-lg">({{ end }} - {{ start }})</span>
  </h2>
  <vue-frappe v-if="labels.length > 0" id="prices" :axisOptions="axisOptions" :labels="labels" type="line" :tooltipOptions="tooltipOptions" :lineOptions="lineOptions" :height="300" :colors="colors" :dataSets="datasets" />
  <div>
    <button @click="retrieveData(30)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">30 day range</button>
    <button @click="retrieveData(20)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">20 day range</button>
    <button @click="retrieveData(1)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">1 day range</button>
  </div>
</div>
</template>
<script>
export default {
  data() {
    return {
      start: '',
      end: '',
      labels: [],
      colors: ['#c0ddf9', '#73b3f3', '#3886e1', '#17459e'],
      lineOptions: {
        regionFill: 0
      },
      axisOptions: {
        xIsSeries: false
      },
      datasets: [{
          name: 'High price',
          chartType: 'line',
          values: []
        },
        {
          name: 'Low price',
          chartType: 'line',
          values: []
        },
        {
          name: 'Open price',
          chartType: 'line',
          values: []
        },
        {
          name: 'Close price',
          chartType: 'line',
          values: []
        }
      ],
      tooltipOptions: {
        formatTooltipX: d => (d + '').toUpperCase(),
        formatTooltipY: d => d + ' EUR',
      },
    }
  },
  created() {
    this.retrieveData(30)
  },
  props: ['propSymbol'],
  computed: {
    symbol() {
      return this.$props.propSymbol
    }
  },
  methods: {
    retrieveData(interval) {
      this.$axios.$get(`${process.env.API_URL}/volume/${this.symbol}/${interval}`).then(res => {
        this.datasets[0].values = res['high']
        this.datasets[1].values = res['low']
        this.datasets[2].values = res['open']
        this.datasets[3].values = res['close']
        this.labels = res['dates']
        this.start = res['start']
        this.end = res['end']
      })
    }
  }
}
</script>
