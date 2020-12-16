<template>
<div class="">
  <ul>
    <li v-for="info in infos" class="even:bg-gray-400 odd:bg-gray-200 p-3">
      <nuxt-link :to="makeLink(info['_id'])" class="text-xl"> <span class="bg-red-500 font-mono text-white px-1">{{ info['_id'] }}</span> {{ info['long_name'] }}</nuxt-link>
    </li>
  </ul>
</div>
</template>

<script>
export default {
  data() {
    return {
      infos: []
    }
  },
  created() {
    this.$axios.$get(`${process.env.API_URL}/infos/short`).then(res => {
      this.infos = res['values']
    })
  },
  methods: {
    makeLink(value) {
      return `/average/${value}`
    }
  }
}
</script>
