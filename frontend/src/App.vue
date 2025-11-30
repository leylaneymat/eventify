<template>
  <Header />
  <div class="event-card-menu">
    <div class="event-cards-container">
      <EventCard v-for="event in events" :key="event.id" :event="event" />
    </div>
  </div>
  <Footer />
</template>

<script>
import Header from '@/components/Header.vue'
import EventCard from '@/components/EventCard.vue'
import Footer from '@/components/Footer.vue'
export default {
  components: { Header, EventCard, Footer },
  data() {
    return { events: [] }
  }
}
</script>
