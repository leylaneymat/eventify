<template>
  <div class="event-card">
    <h3>{{ event.name }}</h3>
    <p>{{ event.description }}</p>
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
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 8px;
}
</style>
