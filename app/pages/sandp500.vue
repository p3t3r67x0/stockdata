<template>
<div>
  <h1 class="text-teal-900 text-xl sm:text-4xl font-bold font-sans mb-6">
    S&P market index
  </h1>
  <table class="border-collapse w-full">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden sm:table-row">
        <th colspan="1" class="text-left px-3 py-3">Ticker</th>
        <th colspan="1" class="text-left px-2 py-3">Date</th>
        <th colspan="1" class="text-left px-2 py-3">Price</th>
        <th colspan="1" class="text-left px-2 py-3">Percentage</th>
      </tr>
    </thead>
    <tbody class="text-md sm:text-xl">
      <tr @click="routeTo(value['symbol'])" v-for="value in values" class="group flex sm:table-row flex-col sm:flex-row flex-wrap sm:flex-no-wrap even:bg-gray-100 odd:bg-gray-300 cursor-pointer mb-3 sm:mb-0">
        <td class="group-hover:bg-blue-300 flex sm:table-cell bg-gray-700 sm:bg-transparent w-full sm:w-auto">
          <div class="flex justify-between sm:justify-start w-full p-1 sm:p-2">
            <span class="order-1 sm:order-2 font-bold sm:font-normal text-white sm:text-gray-900 break-words p-1">{{ value['long_name'] }}</span>
            <span class="order-2 sm:order-1 text-white p-1 text-right">
              <span class="bg-pink-500 rounded font-sans text-white p-1">{{ value['symbol'] }}</span>
            </span>
          </div>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-between sm:table-cell bg-gray-100 sm:bg-transparent w-full sm:w-auto p-2">
          <span>{{ value['data'][1]['date'] }}</span>
          <span class="font-bold">{{ value['data'][1]['close'] }} EUR</span>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-between sm:table-cell bg-gray-300 sm:bg-transparent w-full sm:w-auto p-2">
          <span>{{ value['data'][0]['date'] }}</span>
          <span class="font-bold">{{ value['data'][0]['close'] }} EUR</span>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-end sm:table-cell bg-gray-100 sm:bg-transparent w-full sm:w-auto p-2">
          <span class="text-right">
            <fa v-if="value['percent'] > 0" :icon="['fas', 'arrow-alt-circle-up']" class="text-md sm:text-xl text-green-500 bg-white rounded-full mt-1 mr-1 sm:mr-2" />
            <fa v-if="value['percent'] === 0" :icon="['fas', 'arrow-alt-circle-right']" class="text-md sm:text-xl text-blue-500 bg-white rounded-full mt-1 mr-1 sm:mr-2" />
            <fa v-if="value['percent'] < 0" :icon="['fas', 'arrow-alt-circle-down']" class="text-md sm:text-xl text-red-500 bg-white rounded-full mt-1 mr-1 sm:mr-2" />
            <span class="font-bold">{{ value['percent'] > 0 ? '+' + value['percent'] : value['percent'] }} %</span>
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
    this.$axios.$get(`${process.env.API_URL}/percentages/market/sandp500`).then(res => {
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
