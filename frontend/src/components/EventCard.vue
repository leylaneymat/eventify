<template>
  <div class="event-card">
    <div class="card-header">
      <h3>{{ event.name }}</h3>

      <button class="like-btn" @click="toggleLike">
        <span v-if="isLiked">★</span>
        <span v-else>☆</span>
        {{ likeCount }}
      </button>
    </div>

    <p>{{ event.description }}</p>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const isLiked = ref(props.event.isLiked || false)
    const likeCount = ref(props.event.likes || 0)

    watch(
      () => props.event,
      () => {
        isLiked.value = props.event.isLiked || false
        likeCount.value = props.event.likes || 0
      },
      { deep: true }
    )

    const toggleLike = () => {
      isLiked.value = !isLiked.value
      likeCount.value += isLiked.value ? 1 : -1
    }

    return {
      isLiked,
      likeCount,
      toggleLike
    }
  }
}
</script>

<style scoped>
.event-card {
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 12px;
  background: white;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.like-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
}
</style>
