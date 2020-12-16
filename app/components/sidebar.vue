<template>
<div v-click-outside="hideNav" class="sm:flex sm:min-h-screen h-12 sm:h-auto">
  <div class="fixed w-full top-0 left-0 sm:w-64 overflow-y-auto transition duration-300 transform ease-in overflow-y-auto sm:translate-x-0 sm:static sm:inset-0 z-50 sm:z-0 bg-gray-900">
    <div class="flex justify-center items-center bg-blue-500 sm:border-b-4 sm:border-white h-12 sm:h-16 lg:h-20">
      <p class="tracking-wide font-sans text-white text-2xl sm:text-3xl px-2 sm:px-4">stocklify.xyz</p>
    </div>

    <ul :class="[showNav ? 'block z-50' : 'hidden']" class="sm:block sm:mt-8">
      <li @click="toggleNav" :class="[comparePageName('dashboard') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/symbols">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">Symbols</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('organization') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'columns']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('poll') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none  sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'poll']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('templates') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'mail-bulk']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('calendar') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'calendar-week']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('language') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'font']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('settings') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 sm:focus:outline-none mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'user-cog']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('users') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'users']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('boats') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'ship']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('theme') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'paint-brush']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('event') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/">
          <fa :icon="['fas', 'sticky-note']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" class="sm:hidden text-white border-gray-900 text-white hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100">
        <a class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6">
          <fa :icon="['fas', 'sign-out-alt']" class="col-span-1 mt-1" />
          <span class="col-span-5">Menu entry</span>
        </a>
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
      activeClass: 'bg-gray-600 bg-opacity-25 text-gray-100 border-gray-100',
      inactiveClass: 'border-gray-900 text-white hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100'
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
      return true; // this.pageName === `${value}___${this.$i18n.locale}`
    }
  }
}
</script>
