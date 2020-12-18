<template>
<vue-frappe id="test" :labels="labels" title="Volume" type="axis-mixed" :height="350" :colors="colors" :dataSets="chart">
</vue-frappe>
</template>
<script>
export default {
  data() {
    return {
      colors: ['#4a5568', '#4299e1'],
      labels: [
        '12am-3am', '3am-6am', '6am-9am', '9am-12pm',
        '12pm-3pm', '3pm-6pm', '6pm-9pm', '9pm-12am'
      ],
      chart: [{
          name: "Some Data",
          chartType: 'bar',
          values: [25, 40, 30, 35, 8, 52, 17, -4]
        },
        {
          name: "Yet Another",
          chartType: 'line',
          values: [15, 20, -3, -15, 58, 12, -17, 37]
        }
      ]
    }
  },
  created() {
    this.$axios.$get(`${process.env.API_URL}/volume/${this.symbol}`).then(res => {
      this.chart = res
    })
  },
  props: ['propSymbol'],
  computed: {
    symbol() {
      console.log(this.$props.propSymbol)
      return this.$props.propSymbol
    }
  }
}
</script>
