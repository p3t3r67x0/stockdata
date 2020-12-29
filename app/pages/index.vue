<template>
<div>
  <h1 class="text-teal-900 text-xl sm:text-4xl font-bold font-sans mb-6">
    <span class="text-gray-700">Trending on Stocklify</span>
  </h1>
  <table class="border-collapse w-full">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden sm:table-row">
        <th colspan="1" class="text-left p-3">Ticker</th>
        <th colspan="1" class="text-left p-3">Company</th>
        <th colspan="1" class="text-left p-3">Industry</th>
        <th colspan="1" class="text-left p-3">Clode date</th>
        <th colspan="1" class="text-right p-3">Close price</th>
      </tr>
    </thead>
    <tbody>
      <tr @click="routeTo(value['_id'])" v-for="value in values" class="cursor-pointer flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap even:bg-gray-100 odd:bg-gray-300 mb-3 sm:mb-0">
        <td class="text-left p-3">
          <span class="bg-pink-500 font-sans text-white p-1">{{ value['_id'] }}</span>
        </td>
        <td class="text-left p-3">
          {{ value['long_name'] }}
        </td>
        <td class="text-left p-3">
          {{ value['industry'] }}
        </td>
        <td class="text-left p-3">
          {{ value['timestamp'] }}
        </td>
        <td class="text-right p-3">
          {{ value['close_eur'] }} EUR
        </td>
      </tr>
    </tbody>
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
    this.$axios.$get(`${process.env.API_URL}/newcommers/all`).then(res => {
      this.values = res['values']
    })
  },
  methods: {
    routeTo(value) {
      this.$router.push({
        name: 'average-symbol',
        params: {
          symbol: value.toLowerCase()
        }
      })
    }
  }
}
</script>
