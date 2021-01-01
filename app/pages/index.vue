<template>
<div>
  <h1 class="text-teal-900 text-xl lg:text-4xl font-bold font-sans mb-6">
    <span class="text-gray-700">Trending on Stocklify</span>
  </h1>
  <table class="lg:table-fixed border-collapse w-full">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden lg:table-row">
        <th colspan="1" class="lg:w-5/12 text-left px-3 py-3">Ticker</th>
        <th colspan="1" class="lg:w-4/12 text-left px-2 py-3">Industry</th>
        <th colspan="1" class="lg:w-2/12 text-left px-2 py-3">Close price date</th>
        <th colspan="1" class="lg:w-1/12 text-right px-2 py-3">Close price</th>
      </tr>
    </thead>
    <tbody class="text-md lg:text-xl">
      <tr @click="routeTo(value['_id'])" v-for="value in values" class="group flex lg:table-row flex-col lg:flex-row flex-wrap lg:flex-no-wrap even:bg-gray-100 odd:bg-gray-300 cursor-pointer mb-3 lg:mb-0">
        <td class="group-hover:bg-blue-300 flex lg:table-cell bg-gray-700 lg:bg-transparent w-full lg:w-auto">
          <div class="flex justify-between lg:justify-start w-full p-1 lg:p-2">
            <span class="order-1 lg:order-2 float-left font-bold lg:font-normal text-white lg:text-gray-900 break-words p-1 lg:py-0">{{ value['long_name'] }}</span>
            <span class="order-2 lg:order-1 float-left text-white text-right">
              <span class="bg-pink-500 font-sans text-white p-1">{{ value['_id'] }}</span>
            </span>
          </div>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-between lg:table-cell bg-gray-100 lg:bg-transparent w-full lg:w-auto p-2">
          <span class="font-normal">{{ value['industry'] }}</span>
        </td>
        <td class="group-hover:bg-blue-300 flex justify-between lg:table-cell bg-gray-300 lg:bg-transparent w-full lg:w-auto p-2">
          <span>{{ value['timestamp'] }}</span>
          <span class="font-bold lg:hidden">{{ value['close_eur'] }} EUR</span>
        </td>
        <td class="hidden group-hover:bg-blue-300 lg:table-cell bg-gray-100 lg:bg-transparent text-right w-full lg:w-auto p-2">
          <span class="font-bold">{{ value['close_eur'] }} EUR</span>
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
