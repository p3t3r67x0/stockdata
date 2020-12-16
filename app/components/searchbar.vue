<template>
<header class="hidden sm:flex justify-between items-center border-b-4 border-blue-500 h-16 lg:h-20 px-3 py-3 lg:px-6">
  <div class="w-full flex justify-between items-center">
    <div class="w-full md:w-6/12 lg:w-5/12 xl:w-3/12 relative">
      <div v-click-outside="toggleSearch" @keydown.esc="toggleSearch" class="relative">
        <input v-model="searchTerm" @input="lookupSearchTerm" type="text" class="w-full rounded border focus:outline-none p-2">

        <div v-if="results.length > 0" class="w-full absolute z-30">
          <div @click="setSerchTerm(result)" class="hover:bg-gray-300 bg-gray-200 border shadow p-3 cursor-pointer" v-for="result in results">
            <span class="leading-5 text-gray-900"><strong>{{ result['symbol'] }}</strong>, {{ result['long_name'] }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</header>
</template>

<script>
export default {
  data() {
    return {
      results: [],
      showDropdown: false,
      searchTerm: ''
    }
  },
  methods: {
    toggleSearch() {
      this.results = []
    },
    setSerchTerm(object) {
      this.searchTerm = `${object['symbol']}, ${object['long_name']}`
      this.toggleSearch()
    },
    hideDropdown() {
      return this.showDropdown = false
    },
    toggleDropdown() {
      return this.showDropdown = !this.showDropdown
    },
    retrieveAverages() {
      this.$axios({
        method: 'GET',
        url: `${process.env.API_URL}/query/${this.searchTerm}`,
        validateStatus: () => true
      }).then(res => {
        if (res.status === 200) {}
      })
    },
    lookupSearchTerm() {
      if (this.searchTerm.length >= 1) {
        this.$axios({
          method: 'GET',
          url: `${process.env.API_URL}/query/${this.searchTerm}`,
          validateStatus: () => true
        }).then(res => {
          this.results = []

          if (res.status === 200) {
            if ('results' in res.data) {
              this.results = res.data['results'] || []

              this.$axios.$get()
            }
          }
        })
      } else {
        this.results = []
      }
    }
  }
}
</script>
