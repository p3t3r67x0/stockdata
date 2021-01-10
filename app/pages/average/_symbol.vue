<template>
<div>
  <div v-if="values && 'symbol' in values" class="mb-6">
    <h1 class="text-teal-900 text-xl sm:text-4xl font-bold font-sans mb-6">
      <span class="bg-red-500 text-white px-1">{{ values['symbol'] }}</span>
      <span>{{ values['long_name']}}</span>
    </h1>

    <chart :propSymbol="values['symbol']" />
  </div>

  <table v-if="values && 'averages' in values" class="border-collapse w-full mb-6">
    <thead class="bg-gray-700 text-white text-md">
      <tr class="hidden sm:table-row">
        <th colspan="1" class="text-left">Ticker</th>
        <th colspan="1" class="text-left">Date</th>
        <th colspan="1" class="text-left">Price</th>
        <th colspan="1" class="text-left">Percentage</th>
      </tr>
    </thead>
    <tbody>
      <tr class="flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap mb-3 sm:mb-0">
        <td class="flex bg-gray-700 text-white w-full">
          <span class="w-full text-md sm:text-xl font-bold break-words p-1">
            High averages
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            1 day
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['high_intra_day']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['high_intra_day']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['high_intra_day']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-300 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            10 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['high_ten_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['high_ten_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['high_ten_days']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            30 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['high_thirty_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['high_thirty_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['high_thirty_days']['value'] }} EUR
          </span>
        </td>
      </tr>
      <tr class="flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap mb-3 sm:mb-0">
        <td class="flex bg-gray-700 text-white w-full">
          <span class="w-full text-md sm:text-xl font-bold break-words p-1">
            Low averages
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            1 day
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['low_intra_day']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['low_intra_day']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['low_intra_day']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-300 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            10 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['low_ten_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['low_ten_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['low_ten_days']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            30 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['low_thirty_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['low_thirty_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['low_thirty_days']['value'] }} EUR
          </span>
        </td>
      </tr>
      <tr class="flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap mb-3 sm:mb-0">
        <td class="flex bg-gray-700 text-white w-full">
          <span class="w-full text-md sm:text-xl font-bold break-words p-1">
            Open averages
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            1 day
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['open_intra_day']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['open_intra_day']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['open_intra_day']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-300 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            10 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['open_ten_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['open_ten_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['open_ten_days']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            30 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['open_thirty_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['open_thirty_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['open_thirty_days']['value'] }} EUR
          </span>
        </td>
      </tr>
      <tr class="flex sm:table-row flex-row sm:flex-row flex-wrap sm:flex-no-wrap mb-3 sm:mb-0">
        <td class="flex bg-gray-700 text-white w-full">
          <span class="w-full text-md sm:text-xl font-bold break-words p-1">
            Close averages
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            1 day
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['close_intra_day']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['close_intra_day']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['close_intra_day']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-300 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            10 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['close_ten_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['close_ten_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['close_ten_days']['value'] }} EUR
          </span>
        </td>
        <td class="flex bg-gray-100 text-gray-900 w-full">
          <span class="w-3/12 p-1">
            30 days
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['close_thirty_days']['end'] }}
          </span>
          <span class="w-3/12 p-1">
            {{ values['averages']['close_thirty_days']['start'] }}
          </span>
          <span class="w-3/12 text-right font-bold p-1">
            {{ values['averages']['close_thirty_days']['value'] }} EUR
          </span>
        </td>
      </tr>
    </tbody>
  </table>

  <div class="text-lg">
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Address</h2>
    <p v-if="values && 'long_name' in values" class="mb-1">{{ values['long_name'] }}</p>
    <p v-if="values && 'address' in values" class="mb-1">{{ values['address'] }}</p>
    <p class="mb-1">
      <span v-if="values && 'zip' in values">{{ values['zip'] }}</span>
      <span v-if="values && 'city' in values">{{ values['city'] }}</span>
    </p>
    <p v-if="values && 'country' in values" class="mb-1">{{ values['country'] }}</p>
    <p v-if="values && 'website' in values" class="mb-3">
      <a :href="values['website']" target="_blank" class="text-blue-500 hover:text-blue-700 focus:outline-none">{{ values['website'] }}</a>
    </p>
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Description</h2>
    <p v-if="values && 'long_business_summary' in values">{{ values['long_business_summary'] }}</p>
  </div>
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
    this.$axios.$get(`${process.env.API_URL}/average/${this.$route.params.symbol}`).then(res => {
      this.values = res
    })
  }
}
</script>
