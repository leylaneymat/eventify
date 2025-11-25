<template>
    <div class="event-card">
      <!-- EventCard component -->
    </div>
  </template>
  
  <script>
  export default {
    props: {
      event: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  .event-card {
    width: 100%;
  }
  </style>
  