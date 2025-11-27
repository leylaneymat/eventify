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
