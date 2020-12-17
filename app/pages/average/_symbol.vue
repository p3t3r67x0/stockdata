<template>
<div>
  <div v-if="'symbol' in avgData" class="mb-6">
    <h1 class="text-teal-900 text-4xl font-bold font-sans mb-6">
      <span class="bg-red-500 text-white px-1">{{ avgData['symbol'] }}</span>
      <span>{{ avgData['long_name']}}</span>
    </h1>
  </div>
  <table v-if="'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">High 2 days</td>
      <td class="p-3">{{ avgData['averages']['high_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['high_two_days']['value'] }} EUR</td>
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
  <table v-if="'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Low 2 days</td>
      <td class="p-3">{{ avgData['averages']['low_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['low_two_days']['value'] }} EUR</td>
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
  <table v-if="'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Open 2 days</td>
      <td class="p-3">{{ avgData['averages']['open_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['open_two_days']['value'] }} EUR</td>
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
  <table v-if="'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Close 2 days</td>
      <td class="p-3">{{ avgData['averages']['close_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['close_two_days']['value'] }} EUR</td>
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
  <table v-if="'averages' in avgData" class="table-fixed w-full mb-6">
    <tr class="bg-gray-700 text-white text-md">
      <th class="w-2/6 text-left p-3">Unit</th>
      <th class="w-1/6 text-left p-3">Start</th>
      <th class="w-1/6 text-left p-3">End</th>
      <th class="w-1/6 text-left p-3">Average</th>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Adjust close 2 days</td>
      <td class="p-3">{{ avgData['averages']['adjust_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages']['adjust_two_days']['value'] }} EUR</td>
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
  <div class="text-lg">
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Address</h2>
    <p v-if="'long_name' in avgData" class="mb-1">{{ avgData['long_name'] }}</p>
    <p v-if="'address' in avgData" class="mb-1">{{ avgData['address'] }}</p>
    <p class="mb-1">
      <span v-if="'zip' in avgData">{{ avgData['zip'] }}</span>
      <span v-if="'city' in avgData">{{ avgData['city'] }}</span>
    </p>
    <p v-if="'country' in avgData" class="mb-1">{{ avgData['country'] }}</p>
    <p v-if="'website' in avgData" class="mb-3">
      <a :href="avgData['website']" target="_blank" class="text-blue-500 hover:text-blue-700 focus:outline-none">{{ avgData['website'] }}</a>
    </p>
    <h2 class="text-teal-900 text-xl font-bold font-sans mb-1">Description</h2>
    <p v-if="'long_business_summary' in avgData">{{ avgData['long_business_summary'] }}</p>
  </div>
  <div class="gf-card__chart">
    <linechart :options="{ width: 580, height: 180 }" :dataset="dataset" />
  </div>
</div>
</template>

<script>
import {
  max
} from "d3"

import moment from "moment"
import data from "@/assets/data"

export default {
  data() {
    return {
      data: [],
      avgData: [],
      maxValue: 0,
      filter: null
    }
  },
  filters: {
    formatDate(date) {
      return date ? moment(date).format("MMM DD, HH:MM") : ""
    }
  },
  created() {
    this.maxValue = max(data, d => d.high).toFixed(2)

    this.$axios.$get(`${process.env.API_URL}/average/${this.$route.params.symbol}`).then(res => {
      this.avgData = res
    })
  },
  computed: {
    name() {
      return this.$route.name
    },
    dataset() {
      if (this.filter) {
        if (this.filter[1] === "y") {
          const maxDate = max(data, d => d.date)
          const numberOfYears = parseInt(this.filter[0])
          const yearsAgo = moment(maxDate).subtract(numberOfYears, "years")
          const filtered = data.filter(item => {
            return (
              new Date(item.date) >= new Date(yearsAgo.format()) &&
              new Date(item.date) <= new Date(maxDate)
            )
          })

          return this.transformData(filtered)
        }

        if (this.filter[1] === "m") {
          const numberOfMonths = parseInt(this.filter[0])
          const maxDate = max(data, d => d.date)
          const monthsAgo = moment(maxDate).subtract(numberOfMonths, "months")
          const filtered = data.filter(item => {
            return (
              new Date(item.date) >= new Date(monthsAgo.format()) &&
              new Date(item.date) <= new Date(maxDate)
            )
          })

          return this.transformData(filtered)
        }

        if (this.filter[1] === "d" || this.filter[2] === "d") {
          const numberOfDays = this.filter[2] ?
            parseInt(`${this.filter[0]}${this.filter[1]}`) :
            parseInt(this.filter[0])
          const maxDate = max(data, d => d.date)
          const daysAgo = moment(maxDate).subtract(numberOfDays, "days")
          const filtered = data.filter(item => {
            return (
              new Date(item.date) >= new Date(daysAgo.format()) &&
              new Date(item.date) <= new Date(maxDate)
            )
          })

          return this.transformData(filtered)
        }
      }

      return this.transformData(data)
    }
  },
  methods: {
    transformData(data, limit) {
      const result = []
      const length = limit || data.length

      for (let i = 0; i < length; i++) {
        result.push({
          x: new Date(data[i].date),
          y: data[i].high
        })
      }

      return result
    }
  }
}
</script>
