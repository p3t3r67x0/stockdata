<template>
<div>
  <vue-frappe id="prices" :labels="labels1" type="line" :height="350" :colors="colors1" :dataSets="chart1" />
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
      labels1: [],
      colors1: ['red', 'orange', 'purple', '#4a5568'],
      chart1: [{
        name: 'High price',
        chartType: 'line',
        values: []
      }, {
        name: 'Low price',
        chartType: 'line',
        values: []
      }, {
        name: 'Open price',
        chartType: 'line',
        values: []
      }, {
        name: 'Close price',
        chartType: 'line',
        values: []
      }]
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
        this.chart1[0].values = res['high']
        this.chart1[1].values = res['low']
        this.chart1[2].values = res['open']
        this.chart1[3].values = res['close']
        this.labels1 = res['dates']
      })
    }
  }
}
</script>
