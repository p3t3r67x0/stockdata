<template>
<div v-click-outside="hideNav" class="sm:flex sm:min-h-screen h-12 sm:h-auto">
  <div class="fixed w-full top-0 left-0 sm:w-64 overflow-y-auto transition duration-300 transform ease-in overflow-y-auto sm:translate-x-0 sm:static sm:inset-0 z-50 sm:z-0 bg-gray-900">
    <div class="flex justify-between sm:justify-center items-center bg-blue-500 sm:border-b-4 sm:border-white h-12 sm:h-16 lg:h-20">
      <nuxt-link to="/" class="tracking-wide font-sans text-white text-2xl sm:text-3xl px-2 sm:px-4">stocklify.xyz</nuxt-link>

      <div @click="toggleNav" class="flex flex-cols sm:hidden focus:outline-none overflow-hidden cursor-pointer mr-3">
        <svg class="w-5 h-5 text-white hover:text-white focus:outline-none fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <title>Menu</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path>
        </svg>
      </div>
    </div>

    <ul :class="[showNav ? 'block z-50' : 'hidden']" class="sm:block sm:mt-8">
      <li @click="toggleNav" :class="[comparePageName('dax30') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/dax30">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">DAX 30</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('mdax') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/mdax">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">M DAX</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('sdax') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/sdax">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">S DAX</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('tecdax') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/tecdax">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">TecDAX</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('djia') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/djia">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">Dow Jones</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('sandp500') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/sandp500">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">S&amp;P 500</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('cac30') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/cac30">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">CAC 30</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('aex25') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/aex25">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">AEX 25</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('hsi') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/hsi">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">HSI</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('nse') ? activeClass : inactiveClass]" class="text-white border-b sm:border-b-0 border-gray-700">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/nse">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">NSE</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('symbols') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/symbols">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">Market</span>
        </nuxt-link>
      </li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      showNav: false,
      activeClass: 'bg-gray-600 bg-opacity-25 text-gray-100',
      inactiveClass: 'text-white hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100'
    }
  },
  computed: {
    pageName() {
      return this.$route.name
    }
  },
  methods: {
    hideNav() {
      return this.showNav = false
    },
    toggleNav() {
      return this.showNav = !this.showNav
    },
    comparePageName(value) {
      return this.pageName === value
    }
  }
}
</script>
