<template>
<div>
  <vue-frappe id="prices" :labels="labels1" type="line" :height="350" :colors="colors1" :dataSets="chart1" />
</div>
</template>
<script>
export default {
  data() {
    return {
      labels1: [],
      colors1: ['red', 'orange', 'purple', 'green'],
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
      this.chart1[0].values = res['high']
      this.chart1[1].values = res['low']
      this.chart1[2].values = res['open']
      this.chart1[3].values = res['close']
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
