<template>
<div>
  <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">
    <span>Price chart</span>
    <span v-if="start !== '' && end !== ''" class="font-normal text-lg">({{ end }} - {{ start }})</span>
  </h2>
  <client-only>
    <trading-vue :data="tradingVue" colorCross="#454634" colorTextHL="#ffffff" colorGrid="#a3a3a3" colorText="#3d3333" colorBack="#ffffff" titleTxt="" :width="1220" :height="450" />
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
  props: ['propSymbol'],
  computed: {
    symbol() {
      return this.$props.propSymbol
    }
  },
  methods: {
    retrieveData(interval) {
      this.$axios.$get(`${process.env.API_URL}/volume/${this.symbol}/${interval}`).then(res => {
        this.tradingVue = this.$DataCube ? new this.$DataCube({
          chart: {
            type: 'Candles',
            data: res['values']
          }
        }) : {},
        this.start = res['start']
        this.end = res['end']
      })
    }
  }
}
</script>
