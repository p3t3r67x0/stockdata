<template>
<div>
  <vue-frappe id="volumes" :labels="labels" :axisOptions="axisOptions" type="bar" :height="300" :colors="colors" :dataSets="datasets" />
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
      labels: [],
      colors: ['#4a5568'],
      axisOptions: {
        xAxisMode: 'tick'
      },
      datasets: [{
        name: 'Volume',
        chartType: 'bar',
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
        this.datasets[0].values = res['volumes']
        this.labels = res['dates']
      })
    }
  }
}
</script>
