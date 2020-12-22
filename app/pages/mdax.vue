<template>
<div>
  <h1 class="text-teal-900 text-4xl font-bold font-sans mb-6">
    MDAX market index
  </h1>
  <table v-if="values.length > 0" class="table-fixed w-full">
    <tr class="bg-gray-700 text-white text-md">
      <th colspan="1" class="text-left p-3">Ticker</th>
      <th colspan="1" class="text-left p-3">Last & Current date</th>
      <th colspan="1" class="text-left p-3">Last & Current price</th>
      <th colspan="1" class="text-left p-3">Percentage</th>
    </tr>
    <tr v-for="value in values" :class="[value['percent'] >= 0 ? 'even:bg-green-100 odd:bg-green-200' : 'even:bg-red-300 odd:bg-red-200']">
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(value['symbol'])" class="text-xl sm:text-2xl block">
          <span class="bg-blue-500 font-sans text-white px-1">{{ value['symbol'] }}</span>
        </nuxt-link>
      </td>
      <td colspan="3" class="p-3">
        <table class="table-fixed w-full">
          <tr>
            <td class="py-1">
              <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">
                <span>{{ value['data'][1]['date'] }}</span><br>
              </nuxt-link>
            </td>
            <td class="px-3 py-1">
              <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">
                <span>{{ value['data'][1]['close'] }} EUR</span>
              </nuxt-link>
            </td>
            <td class="px-3">
            </td>
          </tr>
          <tr>
            <td class="py-1">
              <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">
                <span>{{ value['data'][0]['date'] }}</span><br>
              </nuxt-link>
            </td>
            <td class="px-3 py-1">
              <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">
                <span>{{ value['data'][0]['close'] }} EUR</span>
              </nuxt-link>
            </td>
            <td class="px-3">
              <nuxt-link :to="makeLink(value['symbol'])" class="text-xl block">{{ value['percent'] > 0 ? '+' + value['percent'] : value['percent'] }} %</nuxt-link>
            </td>
          </tr>
        </table>
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
