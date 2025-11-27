<template>
  <el-card class="event-card">
    <template #header>
      <div class="card-header">
        <h3>{{ event.name }}</h3>
        <div class="header-actions">
          <el-button type="text" @click="toggleLike">
            <el-icon v-if="event.isLiked">
              <StarFilled />
            </el-icon>
            <el-icon v-else>
              <Star />
            </el-icon>
            {{ event.likes || 0 }}
          </el-button>
        </div>
      </div>
    </template>

    <div class="card-content">
      <p>{{ event.description }}</p>

      <div class="ticket-list">
        <h4>Tickets</h4>
        <el-table :data="event.tickets" style="width: 100%">
          <el-table-column prop="name" label="Name" />
          <el-table-column prop="price" label="Price" />
        </el-table>
      </div>
    </div>
  </el-card>
</template>


<script>
import { ref } from 'vue'
import { Star, StarFilled } from '@element-plus/icons-vue'

export default {
  props: {
    event: { type: Object, required: true }
  },
  setup(props) {
    const toggleLike = () => {
      props.event.isLiked = !props.event.isLiked
      props.event.likes =
        (props.event.likes || 0) + (props.event.isLiked ? 1 : -1)
    }

    return { toggleLike }
  },
  components: { Star, StarFilled }
}
</script>


<style scoped>
.event-card {
  width: 100%;
  max-width: 600px;
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.ticket-list {
  margin-top: 16px;
}
</style>
