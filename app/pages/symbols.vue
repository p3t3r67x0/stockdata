<template>
<div>
  <h1 class="text-teal-900 text-xl sm:text-4xl font-bold font-sans mb-6">
    International markets
  </h1>
  <table v-if="values.length > 0" class="border-collapse w-full">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden sm:table-row">
        <th colspan="1" class="text-left">Ticker</th>
        <th colspan="1" class="text-left">Company</th>
        <th colspan="1" class="text-left">ISIN</th>
      </tr>
    </thead>
    <tbody>
      <tr @click="routeTo(value['_id'])" v-for="value in values" class="flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap mb-3 sm:mb-0">
        <td class="flex bg-gray-700 text-white w-full">
          <span class="w-8/12 text-md sm:text-xl font-bold break-words p-1">{{ value['long_name'] }}</span>
          <span class="w-4/12 text-white p-1 text-right">
            <span class="bg-indigo-500 font-sans text-white p-1">{{ value['_id'] }}</span>
          </span>
        </td>
        <td class="flex bg-gray-300 w-full">
          <span class="w-4/12 text-white p-1">
            <span class="text-gray-900 p-1">
              {{ value['isin'] }}
            </span>
          </span>
          <span class="w-8/12 flex text-gray-900 text-md sm:text-xl p-1">
            
          </span>
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
    this.$axios.$get(`${process.env.API_URL}/symbols/all`).then(res => {
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
