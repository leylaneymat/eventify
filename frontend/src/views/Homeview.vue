<template>
  <div class="event-card-menu">
    <div class="event-cards-container">
      <EventCard v-for="event in events" :key="event.id" :event="event" />
    </div>
  </div>
</template>

<script>
import api from "@/utils/axiosConfig";
import EventCard from "@/components/EventCard.vue";

export default {
  components: { EventCard },

  data() {
    return {
      events: []
    };
  },

  async created() {
    const res = await api.get("api/v1/events/");
    this.events = res.data;
  }
};
</script>
