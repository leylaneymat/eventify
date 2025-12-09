<template>
  <Header />

  <div class="event-card-menu">
    <div class="event-cards-container">
      <EventCard
        v-for="event in events"
        :key="event.id"
        :event="event"
      />
    </div>
  </div>

  <Footer />
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/utils/axiosConfig"
import Header from "@/components/Header.vue"
import EventCard from "@/components/EventCard.vue"
import Footer from "@/components/Footer.vue"

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

<style>
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
