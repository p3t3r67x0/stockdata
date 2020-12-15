<template>
<div>
  <table v-if="'averages' in avgData && avgData.averages.length > 0" class="table-fixed w-full mb-6">
    <tr class="bg-teal-900 text-white text-md">
      <th class="w-2/6 text-left px-3 py-1">Unit</th>
      <th class="w-1/6 text-left px-3 py-1">Start</th>
      <th class="w-1/6 text-left px-3 py-1">End</th>
      <th class="w-1/6 text-left px-3 py-1">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">High 2 days</td>
      <td class="p-3">{{ avgData['averages'][0]['high_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['high_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['high_two_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">High 10 days</td>
      <td class="p-3">{{ avgData['averages'][0]['high_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['high_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['high_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">High 30 days</td>
      <td class="p-3">{{ avgData['averages'][0]['high_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['high_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['high_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="'averages' in avgData && avgData.averages.length > 0" class="table-fixed w-full mb-6">
    <tr class="bg-teal-900 text-white text-md">
      <th class="w-2/6 text-left px-3 py-1">Unit</th>
      <th class="w-1/6 text-left px-3 py-1">Start</th>
      <th class="w-1/6 text-left px-3 py-1">End</th>
      <th class="w-1/6 text-left px-3 py-1">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Low 2 days</td>
      <td class="p-3">{{ avgData['averages'][0]['low_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['low_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['low_two_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Low 10 days</td>
      <td class="p-3">{{ avgData['averages'][0]['low_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['low_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['low_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Low 30 days</td>
      <td class="p-3">{{ avgData['averages'][0]['low_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['low_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['low_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="'averages' in avgData && avgData.averages.length > 0" class="table-fixed w-full mb-6">
    <tr class="bg-teal-900 text-white text-md">
      <th class="w-2/6 text-left px-3 py-1">Unit</th>
      <th class="w-1/6 text-left px-3 py-1">Start</th>
      <th class="w-1/6 text-left px-3 py-1">End</th>
      <th class="w-1/6 text-left px-3 py-1">Average</th>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Open 2 days</td>
      <td class="p-3">{{ avgData['averages'][0]['open_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['open_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['open_two_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Open 10 days</td>
      <td class="p-3">{{ avgData['averages'][0]['open_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['open_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['open_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Open 30 days</td>
      <td class="p-3">{{ avgData['averages'][0]['open_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['open_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['open_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="'averages' in avgData && avgData.averages.length > 0" class="table-fixed w-full mb-6">
    <tr class="bg-teal-900 text-white text-md">
      <th class="w-2/6 text-left px-3 py-1">Unit</th>
      <th class="w-1/6 text-left px-3 py-1">Start</th>
      <th class="w-1/6 text-left px-3 py-1">End</th>
      <th class="w-1/6 text-left px-3 py-1">Average</th>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Close 2 days</td>
      <td class="p-3">{{ avgData['averages'][0]['close_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['close_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['close_two_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Close 10 days</td>
      <td class="p-3">{{ avgData['averages'][0]['close_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['close_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['close_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Close 30 days</td>
      <td class="p-3">{{ avgData['averages'][0]['close_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['close_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['close_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
  <table v-if="'averages' in avgData && avgData.averages.length > 0" class="table-fixed w-full mb-6">
    <tr class="bg-teal-900 text-white text-md">
      <th class="w-2/6 text-left px-3 py-1">Unit</th>
      <th class="w-1/6 text-left px-3 py-1">Start</th>
      <th class="w-1/6 text-left px-3 py-1">End</th>
      <th class="w-1/6 text-left px-3 py-1">Average</th>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Adjust close 2 days</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_two_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_two_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_two_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-100 text-lg">
      <td class="font-bold p-3">Adjust close 10 days</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_ten_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_ten_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_ten_days']['value'] }} EUR</td>
    </tr>
    <tr class="bg-gray-300 text-lg">
      <td class="font-bold p-3">Adjust close 30 days</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_thirty_days']['end'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_thirty_days']['start'] }}</td>
      <td class="p-3">{{ avgData['averages'][0]['adjust_thirty_days']['value'] }} EUR</td>
    </tr>
  </table>
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
  },
  computed: {
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

      // Default
      return this.transformData(data)
    }
  },
  filters: {
    formatDate(date) {
      return date ? moment(date).format("MMM DD, HH:MM") : ""
    }
  },
  created() {
    this.maxValue = max(data, d => d.high).toFixed(2)

    this.$axios.$get('http://localhost:8000/average/amzn').then(res => {
      this.avgData = res
    })
  }
}
</script>
