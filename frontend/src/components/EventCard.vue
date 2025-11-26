<template>
  <div class="event-card">
    <h3 class="event-title">{{ event.name }}</h3>
    <p class="event-description">{{ event.description }}</p>

    <div class="ticket-info">
      <h4>Tickets</h4>
      <ul>
        <li v-for="ticket in event.tickets" :key="ticket.id">
          {{ ticket.name }} — ${{ ticket.price }}
        </li>
      </ul>
    </div>
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
  padding: 20px;
  border-radius: 12px;
  background: white;
}

.event-title {
  margin-bottom: 8px;
  font-size: 20px;
  font-weight: 600;
}

.event-description {
  margin-bottom: 16px;
  color: #444;
}

.ticket-info ul {
  padding-left: 20px;
}

.ticket-info li {
  margin-bottom: 6px;
}
</style>
