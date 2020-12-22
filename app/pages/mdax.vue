<template>
<div>
  <h1 class="text-teal-900 text-4xl font-bold font-sans mb-6">
    <span class="bg-blue-500 text-white px-1">MDAX</span>
  </h1>
  <table v-if="values.length > 0" class="table-fixed w-full">
    <tr class="bg-gray-700 text-white text-md">
      <th colspan="1" class="text-left p-3">Symbol</th>
      <th colspan="1" class="text-left p-3">Current price</th>
      <th colspan="1" class="text-left p-3">Last price</th>
      <th colspan="1" class="text-left p-3">Percent</th>
    </tr>
    <tr v-for="value in values" :class="[value['percent'] >= 0 ? 'even:bg-green-100 odd:bg-green-200' : 'even:bg-red-100 odd:bg-red-200']">
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(value['symbol'])" class="text-xl sm:text-2xl block"><span class="bg-red-500 font-sans text-white px-1">{{ value['symbol'] }}</span></nuxt-link>
      </td>
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">
          <span>{{ value['data'][0]['date'] }}</span><br>
          <span>{{ value['data'][0]['close'] }} EUR</span>
        </nuxt-link>
      </td>
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">
          <span>{{ value['data'][1]['date'] }}</span><br>
          <span>{{ value['data'][1]['close'] }} EUR</span>
        </nuxt-link>
      </td>
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">{{ value['percent'] > 0 ? '+' + value['percent'] : value['percent'] }} %</nuxt-link>
      </td>
    </tr>
  </table>
</div>
</template>

<script>
export default {
  data() {
    return {
      values: []
    }
  },
  created() {
    this.$axios.$get(`${process.env.API_URL}/percentages/market/mdax`).then(res => {
      this.values = res
    })
  },
  methods: {
    makeLink(value) {
      return `/average/${value}`
    }
  }
}
</script>
