<template>
<div>
  <div>
    <vue-frappe id="volumes" :labels="labels0" type="bar" :height="350" :colors="colors0" :dataSets="chart0" />
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
    this.$axios.$get(`${process.env.API_URL}/volume/${this.symbol}`).then(res => {
      this.chart0[0].values = res['volumes']
      this.chart1[0].values = res['high']
      this.chart1[1].values = res['low']
      this.chart1[2].values = res['open']
      this.chart1[3].values = res['close']
      this.labels0 = res['dates']
      this.labels1 = res['dates']
    })
  },
  props: ['propSymbol'],
  computed: {
    symbol() {
      return this.$props.propSymbol
    }
  }
}
</script>
