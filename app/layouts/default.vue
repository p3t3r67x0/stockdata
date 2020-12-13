<template>
<div class="sm:flex min-h-screen bg-color-page font-roboto">
  <sidebar />

  <div class="sm:flex-1 sm:flex sm:flex-col sm:overflow-hidden">
    <searchbar />

    <main class="sm:flex-1 overflow-x-hidden overflow-y-auto">
      <div class="lg:container mx-auto p-3 lg:px-6 lg:pb-6 lg:pt-10">
        <nuxt />
      </div>
    </main>
  </div>
</div>
</template>
