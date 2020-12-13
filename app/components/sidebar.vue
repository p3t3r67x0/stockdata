<template>
<div v-click-outside="hideNav" class="sm:flex sm:min-h-screen h-12 sm:h-auto">
  <div class="fixed w-full top-0 left-0 sm:w-64 overflow-y-auto transition duration-300 transform ease-in overflow-y-auto sm:translate-x-0 sm:static sm:inset-0 z-50 sm:z-0 bg-gray-900">
    <div class="flex justify-between items-center bg-gray-900 sm:border-b-4 sm:border-gray-900 h-12 sm:h-16 lg:h-20">
      <div>
        <img src="/150.png" class="w-48 sm:w-full sm:object-cover px-2 sm:px-4">
      </div>

      <client-only>
        <div @click="toggleNav" class="block sm:hidden focus:outline-none overflow-hidden cursor-pointer h-12 w-12 pr-3">
          <img src="/150.png" class="h-full w-full object-cover" />
        </div>
      </client-only>
    </div>

    <ul :class="[showNav ? 'block z-50' : 'hidden']" class="sm:block sm:mt-8">
      <li @click="toggleNav" :class="[comparePageName('dashboard') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/dashbrd">
          <fa :icon="['fas', 'chart-line']" class="col-span-1 mt-1" />
          <span class="col-span-5">Dashboard</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('organization') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/organation">
          <fa :icon="['fas', 'columns']" class="col-span-1 mt-1" />
          <span class="col-span-5">Organisation</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('poll') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none  sm:mt-1 py-3 px-3 sm:px-6" to="/poll">
          <fa :icon="['fas', 'poll']" class="col-span-1 mt-1" />
          <span class="col-span-5">Umfragen</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('templates') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/temples">
          <fa :icon="['fas', 'mail-bulk']" class="col-span-1 mt-1" />
          <span class="col-span-5">Vorlagen</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('calendar') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/calenr">
          <fa :icon="['fas', 'calendar-week']" class="col-span-1 mt-1" />
          <span class="col-span-5">Kalender</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('language') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/langue">
          <fa :icon="['fas', 'font']" class="col-span-1 mt-1" />
          <span class="col-span-5">Sprache</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('settings') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 sm:focus:outline-none mt-1 py-3 px-3 sm:px-6" to="/settis">
          <fa :icon="['fas', 'user-cog']" class="col-span-1 mt-1" />
          <span class="col-span-5">Profile</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('users') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/users">
          <fa :icon="['fas', 'users']" class="col-span-1 mt-1" />
          <span class="col-span-5">Nutzer</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('boats') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/boats">
          <fa :icon="['fas', 'ship']" class="col-span-1 mt-1" />
          <span class="col-span-5">Boote</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('theme') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/theme">
          <fa :icon="['fas', 'paint-brush']" class="col-span-1 mt-1" />
          <span class="col-span-5">Theme</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" :class="[comparePageName('event') ? activeClass : inactiveClass]" class="text-white">
        <nuxt-link class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6" to="/event">
          <fa :icon="['fas', 'sticky-note']" class="col-span-1 mt-1" />
          <span class="col-span-5">Events</span>
        </nuxt-link>
      </li>
      <li @click="toggleNav" class="sm:hidden text-white border-gray-900 text-white hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100">
        <a class="grid grid-cols-6 focus:outline-none sm:mt-1 py-3 px-3 sm:px-6">
          <fa :icon="['fas', 'sign-out-alt']" class="col-span-1 mt-1" />
          <span class="col-span-5">Logout</span>
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
