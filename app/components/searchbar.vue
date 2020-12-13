<template>
<header class="hidden sm:flex justify-between items-center bg-color-form border-b-4 border-blue-550 h-16 lg:h-20 px-3 py-3 lg:px-6">
  <div class="w-full flex justify-between items-center">
    <div class="hidden sm:block relative ml-3">
      <div @click="toggleDropdown" class="focus:outline-none overflow-hidden cursor-pointer h-10 lg:h-12 w-10 lg:w-12">
        <img src="/150.png" class="h-full w-full object-cover" />
      </div>

      <!-- <ul class="absolute right-0 mt-2 w-48 bg-color-nav overflow-hidden rounded shadow z-20">
        <li @click="toggleDropdown">
          <nuxt-link to="/settings" class="block px-4 py-2 text-sm text-color-nav hover:bg-gray-800 border-b border-color-form">Profile</nuxt-link>
        </li>
        <li @click="toggleDropdown">
          <a class="cursor-pointer block px-4 py-2 text-sm text-color-nav hover:bg-gray-800">Logout</a>
        </li>
      </ul> -->
    </div>
  </div>
</header>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
      searchTerm: '',
      users: []
    }
  },
  computed: {
    avatar() {
      return {
        eyeType: '',
        clotheType: '',
        circleColor: '',
        accessoriesType: '',
        facialHairColor: '',
        facialHairType: '',
        clotheColor: '',
        eyebrowType: '',
        graphicType: '',
        hairColor: '',
        mouthType: '',
        skinColor: '',
        topColor: '',
        topType: ''
      }
    },
    availableLocales() {
      return true; // this.$i18n.locales.filter(i => i.code !== this.$i18n.locale)
    }
  },
  methods: {
    toggleSearch() {
      this.users = []
    },
    setSerchTerm(user) {
      this.searchTerm = user.name
      this.toggleSearch()
    },
    hideDropdown() {
      return this.showDropdown = false
    },
    toggleDropdown() {
      return this.showDropdown = !this.showDropdown
    },
    lookupSearchTerm() {
      if (this.searchTerm.length >= 1) {
        this.$axios({
          method: 'POST',
          url: `${process.env.API_URL}/lookup/users`,
          data: {
            name: this.searchTerm
          },
          validateStatus: () => true
        }).then(res => {
          if (res.status === 200) {
            this.users = res.data || []
          } else {
            console.debug(res.data)
          }
        })
      } else {
        this.users = []
      }
    }
  }
}
</script>
