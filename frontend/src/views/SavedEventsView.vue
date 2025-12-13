<template>
  <div class="saved-events-view">
    <div class="page-header">
      <h1>My Saved Events</h1>
      <p v-if="!loading && savedEvents.length > 0">
        You have {{ savedEvents.length }} saved event{{ savedEvents.length !== 1 ? 's' : '' }}
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading" :size="50">
        <Loading />
      </el-icon>
      <p>Loading your saved events...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="savedEvents.length === 0" class="empty-state">
      <el-icon :size="80"><FolderOpened /></el-icon>
      <h2>No saved events yet</h2>
      <p>Start exploring events and save the ones you're interested in!</p>
      <el-button type="primary" @click="goToHome">Browse Events</el-button>
    </div>

    <!-- Events List -->
    <div v-else class="saved-events-container">
      <EventCard
        v-for="savedEvent in savedEvents"
        :key="savedEvent.id"
        :event="savedEvent.event"
        @unsaved="handleUnsaved"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import EventCard from '@/components/EventCard.vue';
import { Loading, FolderOpened } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const router = useRouter();
const userStore = useUserStore();
const savedEvents = ref([]);
const loading = ref(true);

const toErrorText = (error, fallback) => {
  const detail = error?.response?.data?.detail || error?.message || 'Unknown error';
  return `${fallback}: ${detail}`;
};

const normalizeSavedEvent = (saved) => ({
  ...saved,
  event: {
    ...saved.event,
    isLiked: saved.event?.isLiked ?? saved.event?.is_liked ?? false,
  },
});

const loadSavedEvents = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('Please login to view saved events');
    router.push('/');
    return;
  }

  loading.value = true;
  try {
    await userStore.loadSavedEvents();
    savedEvents.value = userStore.savedEvents.map(normalizeSavedEvent);
  } catch (error) {
    ElMessage.error(toErrorText(error, 'Failed to load saved events'));
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleUnsaved = (eventId) => {
  // Remove from local list when unsaved
  savedEvents.value = savedEvents.value.filter(
    saved => saved.event.id !== eventId
  );
};

const goToHome = () => {
  router.push('/');
};

onMounted(() => {
  loadSavedEvents();
});
</script>

<style scoped>
.saved-events-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.page-header {
  margin-bottom: 32px;
  text-align: center;
}

.page-header h1 {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.page-header p {
  font-size: 16px;
  color: #606266;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  color: #909399;
}

.empty-state h2 {
  font-size: 24px;
  margin: 16px 0 8px;
  color: #606266;
}

.empty-state p {
  font-size: 16px;
  margin-bottom: 24px;
}

.saved-events-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
</style>
