<template>
<div>
  <h1 class="text-teal-900 text-4xl font-bold font-sans mb-6">
    <span class="bg-blue-500 text-white px-1">DAX30</span>
  </h1>
  <table v-if="values.length > 0" class="table-fixed w-full">
    <tr class="bg-gray-700 text-white text-md">
      <th colspan="1" class="text-left p-3">Symbol</th>
      <th colspan="2" class="text-left p-3">Company</th>
      <th colspan="1" class="text-left p-3">ISIN</th>
    </tr>
    <tr v-for="value in values" class="even:bg-gray-400 odd:bg-gray-200">
      <td colspan="1" class="p-3">
        {{ value }}
        <nuxt-link :to="makeLink(value['_id'])" class="text-xl sm:text-2xl block"><span class="bg-red-500 font-sans text-white px-1">{{ value['_id'] }}</span></nuxt-link>
      </td>
      <td colspan="2" class="p-3">
        <nuxt-link :to="makeLink(value['_id'])" class="text-xl block">{{ value['long_name'] }}</nuxt-link>
      </td>
      </td>
      <td colspan="1" class="p-3">
        <nuxt-link :to="makeLink(value['_id'])" class="text-xl block">{{ value['isin'] }}</nuxt-link>
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
    this.$axios.$get(`${process.env.API_URL}/percentages/market/dax30`).then(res => {
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
