<template>
  <div class="event-card-menu">
    <div class="event-cards-container">
      <EventCard v-for="event in events" :key="event.id" :event="event" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/utils/axiosConfig"
import EventCard from "@/components/EventCard.vue"

const events = ref([])

onMounted(async () => {
  try {
    const res = await api.get("/api/v1/events/")
    events.value = res.data
  } catch (err) {
    console.error("Error loading events:", err)
  }
})
</script>

<style scoped>
.event-card-menu {
  padding: 40px 0;
  display: flex;
  justify-content: center;
}

.event-cards-container {
  width: 90%;
  max-width: 1400px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

@media (max-width: 1000px) {
  .event-cards-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .event-cards-container {
    grid-template-columns: 1fr;
  }
}
</style>
