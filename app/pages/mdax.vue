<template>
<div>
  <h1 class="text-teal-900 text-4xl font-bold font-sans mb-6">
    <span class="bg-blue-500 text-white px-1">MDAX</span>
  </h1>
  <table v-if="infos.length > 0" class="table-fixed w-full">
    <tr class="bg-gray-700 text-white text-md">
      <th colspan="1" class="text-left p-3">Symbol</th>
      <th colspan="2" class="text-left p-3">Company</th>
      <th colspan="1" class="text-left p-3">ISIN</th>
    </tr>
    <tr v-for="info in infos" class="even:bg-gray-400 odd:bg-gray-200">
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(info['_id'])" class="text-xl sm:text-2xl block"><span class="bg-red-500 font-sans text-white px-1">{{ info['_id'] }}</span></nuxt-link>
      </td>
      <td colspan="2" class="p-3">
        <nuxt-link :to="makeLink(info['_id'])" class="text-xl block">{{ info['long_name'] }}</nuxt-link>
      </td>
      </td>
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(info['_id'])" class="text-xl block">{{ info['isin'] }}</nuxt-link>
      </td>
    </tr>
  </table>
</div>
</template>

<script>
export default {
  data() {
    return {
      infos: []
    }
  },
  created() {
    this.$axios.$get(`${process.env.API_URL}/symbols/market/mdax`).then(res => {
      this.infos = res['values']
    })
  },
  methods: {
    makeLink(value) {
      return `/average/${value}`
    }
  }
}
</script>
