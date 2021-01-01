<template>
<div>
  <h1 class="text-teal-900 text-xl md:text-4xl font-bold font-sans mb-6">
    DAX market index
  </h1>
  <table class="md:table-fixed border-collapse w-full">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden md:table-row">
        <th colspan="1" class="md:w-4/12 text-left px-3 py-3">Ticker</th>
        <th colspan="1" class="md:w-3/12 text-left px-2 py-3">Date</th>
        <th colspan="1" class="md:w-3/12 text-left px-2 py-3">Price</th>
        <th colspan="1" class="md:w-2/12 text-right px-2 py-3">Percentage</th>
      </tr>
    </thead>
    <tbody class="text-md md:text-xl">
      <tr @click="routeTo(value['symbol'])" v-for="value in values" class="group flex md:table-row flex-col md:flex-row flex-wrap md:flex-no-wrap even:bg-gray-100 odd:bg-gray-300 cursor-pointer mb-3 md:mb-0">
        <td class="group-hover:bg-blue-300 flex md:table-cell bg-gray-700 md:bg-transparent w-full md:w-auto">
          <div class="flex justify-between md:justify-start w-full p-1 md:p-2">
            <span class="order-1 md:order-2 font-bold md:font-normal text-white md:text-gray-900 break-words p-1">{{ value['long_name'] }}</span>
            <span class="order-2 md:order-1 text-white p-1 text-right">
              <span class="bg-pink-500 rounded font-sans text-white p-1">{{ value['symbol'] }}</span>
            </span>
          </div>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-between md:table-cell bg-gray-100 md:bg-transparent w-full md:w-auto p-2">
          <span>{{ value['data'][1]['date'] }}</span>
          <span class="font-bold">{{ value['data'][1]['close'] }} EUR</span>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-between md:table-cell bg-gray-300 md:bg-transparent w-full md:w-auto p-2">
          <span>{{ value['data'][0]['date'] }}</span>
          <span class="font-bold">{{ value['data'][0]['close'] }} EUR</span>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-end md:table-cell bg-gray-100 md:bg-transparent w-full md:w-auto p-2">
          <span class="block text-right">
            <fa v-if="value['percent'] > 0" :icon="['fas', 'arrow-alt-circle-up']" class="text-md md:text-xl text-green-500 bg-white rounded-full mt-1 mr-1 md:mr-2" />
            <fa v-if="value['percent'] === 0" :icon="['fas', 'arrow-alt-circle-right']" class="text-md md:text-xl text-blue-500 bg-white rounded-full mt-1 mr-1 md:mr-2" />
            <fa v-if="value['percent'] < 0" :icon="['fas', 'arrow-alt-circle-down']" class="text-md md:text-xl text-red-500 bg-white rounded-full mt-1 mr-1 md:mr-2" />
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
    this.$axios.$get(`${process.env.API_URL}/percentages/market/dax30`).then(res => {
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
