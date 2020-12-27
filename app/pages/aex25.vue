<template>
<div>
  <h1 class="text-teal-900 text-xl sm:text-4xl font-bold font-sans mb-6">
    <span class="text-gray-700">AEX market index</span>
  </h1>
  <table class="border-collapse w-full">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden sm:table-row">
        <th colspan="1" class="text-left">Ticker</th>
        <th colspan="1" class="text-left">Date</th>
        <th colspan="1" class="text-left">Price</th>
        <th colspan="1" class="text-left">Percentage</th>
      </tr>
    </thead>
    <tbody>
      <tr @click="routeTo(value['symbol'])" v-for="value in values" class="flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap mb-3 sm:mb-0">
        <td class="flex bg-gray-700 text-white w-full">
          <span class="w-8/12 text-md sm:text-xl font-bold break-words p-1">{{ value['long_name'] }}</span>
          <span class="w-4/12 text-white p-1 text-right">
            <span class="bg-indigo-500 font-sans text-white p-1">{{ value['symbol'] }}</span>
          </span>
        </td>
        <td class="flex bg-gray-300 w-full">
          <span class="w-4/12 text-white p-1">
            <span class="text-gray-900 p-1">
              {{ value['data'][1]['date'] }}
            </span>
          </span>
          <span class="w-8/12 flex text-gray-900 text-md sm:text-xl p-1">
            <span class="w-3/5">
              {{ value['data'][1]['close'] }} EUR
            </span>
            <span class="w-2/5" />
          </span>
        </td>
        <td class="flex bg-gray-200 w-full">
          <span class="w-4/12 text-white p-1">
            <span class="text-gray-900 p-1">
              {{ value['data'][0]['date'] }}
            </span>
          </span>
          <span class="w-8/12 flex text-gray-900 text-md sm:text-xl p-1">
            <span class="w-3/5">
              {{ value['data'][0]['close'] }} EUR
            </span>
            <span class="w-2/5 text-right">
              <fa v-if="value['percent'] > 0" :icon="['fas', 'arrow-alt-circle-up']" class="text-md sm:text-xl text-green-500 bg-white rounded-full mt-1 mr-1 sm:mr-4" />
              <fa v-if="value['percent'] === 0" :icon="['fas', 'arrow-alt-circle-right']" class="text-md sm:text-xl text-blue-500 bg-white rounded-full mt-1 mr-1 sm:mr-4" />
              <fa v-if="value['percent'] < 0" :icon="['fas', 'arrow-alt-circle-down']" class="text-md sm:text-xl text-red-500 bg-white rounded-full mt-1 mr-1 sm:mr-4" />
              <span>{{ value['percent'] > 0 ? '+' + value['percent'] : value['percent'] }} %</span>
            </span>
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
    this.$axios.$get(`${process.env.API_URL}/percentages/market/aex25`).then(res => {
      this.values = res
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
