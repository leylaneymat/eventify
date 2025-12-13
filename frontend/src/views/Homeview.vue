<template>
  <div class="home-view">
    <!-- Category Filter -->
    <div class="filter-section">
      <h2>Filter by Category</h2>
      <div class="category-filters">
        <el-tag
          :type="selectedCategory === null ? 'primary' : ''"
          @click="filterByCategory(null)"
          class="category-tag"
          :class="{ active: selectedCategory === null }"
        >
          All Events
        </el-tag>
        <el-tag
          v-for="category in categories"
          :key="category.value"
          :type="selectedCategory === category.value ? 'primary' : ''"
          @click="filterByCategory(category.value)"
          class="category-tag"
          :class="{ active: selectedCategory === category.value }"
        >
          {{ category.label }}
        </el-tag>
      </div>
    </div>

    <!-- Events Grid -->
    <div class="event-card-menu">
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading" :size="50">
          <Loading />
        </el-icon>
        <p>Loading events...</p>
      </div>
      <div v-else-if="events.length === 0" class="no-events">
        <p>No events found in this category.</p>
      </div>
      <div v-else class="event-cards-container">
        <EventCard v-for="event in events" :key="event.id" :event="event" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/utils/axiosConfig"
import EventCard from "@/components/EventCard.vue"
import { Loading } from '@element-plus/icons-vue'

const events = ref([])
const categories = ref([])
const selectedCategory = ref(null)
const loading = ref(true)

// utility: make label pretty (e.g. "concert" -> "Concert")
const prettyLabel = (val) => {
  if (!val || typeof val !== "string") return String(val)
  return val.charAt(0).toUpperCase() + val.slice(1)
}

const normalizeCategories = (raw) => {
  // Expecting either: ['concert','festival'] or [{value:'concert', label:'Concert'}, ...]
  const seen = new Set()
  const out = []

  if (!raw || !Array.isArray(raw)) return out

  for (const item of raw) {
    let value, label
    if (typeof item === "string") {
      value = item
      label = prettyLabel(item)
    } else if (item && typeof item === "object") {
      // item could be {value, label} or {key:...}
      value = item.value ?? item.key ?? item.name
      label = item.label ?? item.name ?? prettyLabel(value)
    }

    if (!value) continue
    const v = String(value)
    if (seen.has(v)) continue
    seen.add(v)
    out.push({ value: v, label })
  }

  return out
}

const ensureOtherPresent = (arr) => {
  const hasOther = arr.some(c => String(c.value).toLowerCase() === "other")
  if (!hasOther) {
    arr.push({ value: "other", label: "Other" })
  }
  return arr
}

const normalizeEvent = (event) => ({
  ...event,
  isLiked: event?.isLiked ?? event?.is_liked ?? false,
})

const mapEventList = (rawEvents) => (rawEvents || []).map(normalizeEvent)

const filterByCategory = async (category) => {
  selectedCategory.value = category
  loading.value = true

  try {
    const url = category
      ? `/api/v1/events/?category=${encodeURIComponent(category)}`
      : '/api/v1/events/'
    const res = await api.get(url)
    // If the API returns an object (pagination) like { results: [...] }, handle both cases:
    const fetched = Array.isArray(res.data) ? res.data : (res.data.results ?? [])
    events.value = mapEventList(fetched)
  } catch (err) {
    console.error("Error loading events:", err)
    events.value = []
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const res = await api.get('/api/v1/events/categories/')
    let raw = res.data
    // normalize into objects {value,label}
    let normalized = normalizeCategories(raw)
    normalized = ensureOtherPresent(normalized)
    categories.value = normalized
  } catch (err) {
    console.error("Error loading categories:", err)
    categories.value = []
  }
}

onMounted(async () => {
  await loadCategories()
  await filterByCategory(null)
})
</script>

<style scoped>
.home-view {
  width: 100%;
}

.filter-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 5%;
}

.filter-section h2 {
  font-size: 20px;
  margin-bottom: 16px;
  color: #303133;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.category-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-tag {
  cursor: pointer;
  padding: 8px 16px;
  font-size: 14px;
  transition: all 0.3s;
}

.category-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.category-tag.active {
  font-weight: bold;
}

.event-card-menu {
  padding: 20px 0 40px;
  display: flex;
  justify-content: center;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #909399;
}

.loading-container p {
  margin-top: 16px;
  font-size: 16px;
}

.no-events {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
  font-size: 16px;
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

  .category-filters {
    gap: 8px;
  }

  .category-tag {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>
