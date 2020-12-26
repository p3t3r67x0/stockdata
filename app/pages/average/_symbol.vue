<template>
<div>
  <div v-if="avgData && 'symbol' in avgData" class="mb-6">
    <h1 class="text-teal-900 text-4xl font-bold font-sans mb-6">
      <span class="bg-red-500 text-white px-1">{{ avgData['symbol'] }}</span>
      <span>{{ avgData['long_name']}}</span>
    </h1>

    <chart-prices :propSymbol="avgData['symbol']" />
  </div>
  <table v-if="avgData && 'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">High intra day</td>
      <td class="p-3">{{ avgData['averages']['high_intra_day']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_intra_day']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_intra_day']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">High 10 days</td>
      <td class="p-3">{{ avgData['averages']['high_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">High 30 days</td>
      <td class="p-3">{{ avgData['averages']['high_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="avgData && 'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Low intra day</td>
      <td class="p-3">{{ avgData['averages']['low_intra_day']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_intra_day']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_intra_day']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Low 10 days</td>
      <td class="p-3">{{ avgData['averages']['low_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Low 30 days</td>
      <td class="p-3">{{ avgData['averages']['low_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="avgData && 'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Open intra day</td>
      <td class="p-3">{{ avgData['averages']['open_intra_day']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_intra_day']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_intra_day']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Open 10 days</td>
      <td class="p-3">{{ avgData['averages']['open_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Open 30 days</td>
      <td class="p-3">{{ avgData['averages']['open_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="avgData && 'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Close intra day</td>
      <td class="p-3">{{ avgData['averages']['close_intra_day']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_intra_day']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_intra_day']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Close 10 days</td>
      <td class="p-3">{{ avgData['averages']['close_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Close 30 days</td>
      <td class="p-3">{{ avgData['averages']['close_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="avgData && 'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Adjust close intra day</td>
      <td class="p-3">{{ avgData['averages']['adjust_intra_day']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_intra_day']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_intra_day']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Adjust close 10 days</td>
      <td class="p-3">{{ avgData['averages']['adjust_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Adjust close 30 days</td>
      <td class="p-3">{{ avgData['averages']['adjust_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <div v-if="avgData && 'symbol' in avgData" class="mb-6">
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Volume chart</h2>
    <chart-volumes :propSymbol="avgData['symbol']" />
  </div>
  <div class="text-lg">
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Address</h2>
    <p v-if="avgData && 'long_name' in avgData" class="mb-1">{{ avgData['long_name'] }}</p>
    <p v-if="avgData && 'address' in avgData" class="mb-1">{{ avgData['address'] }}</p>
    <p class="mb-1">
      <span v-if="avgData && 'zip' in avgData">{{ avgData['zip'] }}</span>
      <span v-if="avgData && 'city' in avgData">{{ avgData['city'] }}</span>
    </p>
    <p v-if="avgData && 'country' in avgData" class="mb-1">{{ avgData['country'] }}</p>
    <p v-if="avgData && 'website' in avgData" class="mb-3">
      <a :href="avgData['website']" target="_blank" class="text-blue-500 hover:text-blue-700 focus:outline-none">{{ avgData['website'] }}</a>
    </p>
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Description</h2>
    <p v-if="avgData && 'long_business_summary' in avgData">{{ avgData['long_business_summary'] }}</p>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      avgData: []
    }
  },
  created() {
    this.$axios.$get(`${process.env.API_URL}/average/${this.$route.params.symbol}`).then(res => {
      this.avgData = res
    })
  }
}
</script>
