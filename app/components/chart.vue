<template>
<div ref="tradingWrapper">
  <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">
    <span>Price chart</span>
    <span v-if="start !== '' && end !== ''" class="font-normal text-lg">({{ end }} - {{ start }})</span>
  </h2>
  <client-only>
    <trading-vue :data="tradingVue" ref="tradingVue" colorCross="#454634" colorTextHL="#ffffff" colorGrid="#a3a3a3" colorText="#3d3333" colorBack="#ffffff" titleTxt="" :width="width" :height="350" />
  </client-only>
  <div>
    <button @click="retrieveData(100)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">30 day range</button>
    <button @click="retrieveData(30)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">20 day range</button>
    <button @click="retrieveData(1)" class="bg-gray-400 text-gray-800 px-3 py-2 rounded focus:outline-none">1 day range</button>
  </div>
</div>
</template>
<script>
export default {
  data() {
    return {
      width: 0,
      start: '',
      end: '',
      tradingVue: this.$DataCube ? new this.$DataCube({
        chart: {
          type: 'Candles',
          data: []
        }
      }) : {}
    }
  },
  created() {
    this.retrieveData(100)
  },
  mounted() {
    this.resizeWidth()
    window.addEventListener('resize', this.resizeWidth)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeWidth)
  },
  computed: {
    symbol() {
      return this.$props.propSymbol
    }
  },
  props: ['propSymbol'],
  methods: {
    resizeWidth(event) {
      if (process.client) {
        this.$nextTick(() => {
          this.width = this.$refs.tradingWrapper.clientWidth
        })
      }
    },
    formatDate(date) {
      const year = new Intl.DateTimeFormat('de', {
        year: 'numeric'
      }).format(date);

      const month = new Intl.DateTimeFormat('de', {
        month: 'short'
      }).format(date);

      const day = new Intl.DateTimeFormat('de', {
        day: '2-digit'
      }).format(date);

      return `${day}. ${month}. ${year}`
    },
    retrieveData(interval) {
      this.$axios.$get(`${process.env.API_URL}/volume/${this.symbol}/${interval}`).then(res => {
        this.$refs.tradingVue.resetChart()

        this.tradingVue = this.$DataCube ? new this.$DataCube({
          chart: {
            type: 'Candles',
            data: res['values']
          }
        }) : {}

        this.$nextTick(() => {
          const t = this.$refs.tradingVue.getRange()

          this.start = this.formatDate(new Date(t[1]))
          this.end = this.formatDate(new Date(t[0]))
        })

        this.resizeWidth()
      })
    }
  }
}
</script>
