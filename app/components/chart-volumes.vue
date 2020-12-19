<template>
<div>
  <vue-frappe id="volumes" :labels="labels0" type="bar" :height="350" :colors="colors0" :dataSets="chart0" />
  <div>
    <button @click="retrieveData(30)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">30 day range</button>
    <button @click="retrieveData(20)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">20 day range</button>
    <button @click="retrieveData(1)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">15 min range</button>
  </div>
</div>
</template>
<script>
export default {
  data() {
    return {
      labels0: [],
      labels1: [],
      colors0: ['#4a5568'],
      colors1: ['red', 'orange', 'purple', 'green'],
      chart0: [{
        name: 'Volume',
        chartType: 'bar',
        values: []
      }],
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
        this.chart0[0].values = res['volumes']
        this.labels0 = res['dates']
      })
    }
  }
}
</script>
