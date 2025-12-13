<template>
  <el-card class="event-card">

    <!-- HEADER -->
    <template #header>
      <div class="card-header">
        <h3 class="event-title">{{ event.name }}</h3>

        <div class="header-actions">
          <el-button type="text" @click="toggleLike">
            <HeartIcon :filled="event.isLiked" />
            {{ event.likes || 0 }}
          </el-button>

          <el-button type="text" @click="showComments = true">
            <el-icon><ChatRound /></el-icon>
            {{ event.comments.length || 0 }}
          </el-button>

          <!-- SAVE BUTTON -->
          <el-button type="text" @click="toggleSave" :title="isSaved ? 'Unsave event' : 'Save event'">
            <el-icon v-if="isSaved" class="saved-icon"><CollectionTag /></el-icon>
            <el-icon v-else><Collection /></el-icon>
          </el-button>
        </div>
      </div>
    </template>
    <!-- CONTENT -->
    <div class="card-content">
      <p class="event-description">{{ event.description }}</p>
      <p class="event-extra"></p>
      <p class="event-date">Date: {{ formattedDate }}</p>
      <p class="event-time">Time: {{ formattedTime }}</p>
      <p class="event-category">Category: {{ event.category }}</p>

      <div class="ticket-list">
        <h4>Tickets</h4>
        <el-table :data="event.tickets" style="width: 100%">
          <el-table-column prop="name" label="Name" />
          <el-table-column label="Price">
            <template #default="scope">
              ₼{{ scope.row.price }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <!-- FOOTER -->
    <template #footer>
      <div class="card-footer">
        <el-button type="primary" @click="openTicketPurchaseDialog">
          Buy Ticket
        </el-button>
      </div>
    </template>

    <!-- COMMENTS DIALOG -->
    <el-dialog v-model="showComments" title="Event Comments">
      <div class="comment-list">
        <div class="comment-header">
          <el-input
            class="comment-box"
            v-model="newComment"
            placeholder="Add a comment"
          />

          <el-button type="primary" @click="addComment">
            Add Comment
          </el-button>
        </div>
        <div v-for="comment in event.comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="commenter">{{ comment.author }}</span>
            <span class="comment-date">{{ comment.createdAt }}</span>
          </div>
          <div class="comment-content">{{ comment.text }}</div>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showTicketPurchaseDialog" title="Purchase Ticket" width="500px">
      <div class="ticket-purchase-container">
        <el-form>
          <el-form-item label="Select Ticket">
            <el-select
              v-model="selectedTicket"
              placeholder="Choose a ticket"
              style="width: 100%"
            >
              <el-option
                v-for="ticket in event.tickets"
                :key="ticket.id"
                :label="`${ticket.name} - ₼${ticket.price}`"
                :value="ticket.id"
              >
                <div class="ticket-option">
                  <span>{{ ticket.name }}</span>
                  <span class="ticket-price">₼{{ ticket.price }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <div class="purchase-actions">
          <el-button
            type="primary"
            @click="buyTicket"
            :disabled="!selectedTicket"
          >
            Buy
          </el-button>
        </div>
      </div>
    </el-dialog>

  </el-card>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { ChatRound, Collection, CollectionTag } from '@element-plus/icons-vue';
import HeartIcon from "@/components/HeartIcon.vue";
import { useUserStore } from '@/stores/userStore';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  emits: ['unsaved'],
  setup(props, { emit }) {
    const showComments = ref(false);
    const newComment = ref('');
    const userStore = useUserStore();
    const showTicketPurchaseDialog = ref(false);
    const selectedTicket = ref(null);
    const isSaved = ref(false);
    const formatDate = (dateStr) => {
      const dateObj = new Date(dateStr);
      if (Number.isNaN(dateObj.getTime())) return '';
      const day = String(dateObj.getDate()).padStart(2, '0');
      const month = String(dateObj.getMonth() + 1).padStart(2, '0');
      const year = dateObj.getFullYear();
      return `${day}.${month}.${year}`;
    };

    const formatTime = (dateStr) => {
      const dateObj = new Date(dateStr);
      if (Number.isNaN(dateObj.getTime())) return '';
      const hours = String(dateObj.getHours()).padStart(2, '0');
      const minutes = String(dateObj.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    };

    const formattedDate = computed(() => formatDate(props.event.date));
    const formattedTime = computed(() => formatTime(props.event.date));

    const toErrorText = (error, fallback) => {
      const detail = error?.response?.data?.detail || error?.message || 'Unknown error';
      return `${fallback}: ${detail}`;
    };

    // Check if event is saved on mount
    const checkSavedStatus = async () => {
      if (userStore.isLoggedIn) {
        isSaved.value = await userStore.checkEventSaved(props.event.id);
      }
    };

    const ensureLikeFlag = () => {
      // normalize server snake_case flag into the camelCase field the UI expects
      if (props.event && props.event.isLiked === undefined) {
        props.event.isLiked = !!props.event.is_liked;
      }
    };

    onMounted(() => {
      checkSavedStatus();
      ensureLikeFlag();
    });

    const toggleSave = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login to save events');
        return;
      }

      try {
        if (isSaved.value) {
          const result = await userStore.unsaveEvent(props.event.id);
          if (result) {
             emit('unsaved', props.event.id);
          }
          isSaved.value = false;
          ElMessage.success('Event removed from saved list');
        } else {
          await userStore.saveEvent(props.event.id);
          isSaved.value = true;
          ElMessage.success('Event saved successfully');
        }
      } catch (error) {
        ElMessage.error(toErrorText(error, 'Failed to update saved status'));
        console.error(error);
      }
    };

    const toggleLike = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login to like events');
        return;
      }

      try {
        if (!props.event.isLiked) {
          const response = await axios.post(`http://localhost:8000/api/v1/events/${props.event.id}/likes/`);
          localStorage.setItem('likeObj', JSON.stringify(response.data));
        } else {
          let likeObj = JSON.parse(localStorage.getItem('likeObj'));
          await axios.delete(`http://localhost:8000/api/v1/events/${props.event.id}/likes/${likeObj.id}/`);
          localStorage.removeItem('likeObj');
        }

        props.event.isLiked = !props.event.isLiked;
        props.event.likes = (props.event.likes || 0) + (props.event.isLiked ? 1 : -1);
      } catch (error) {
        let likeObj = JSON.parse(localStorage.getItem('likeObj')) || null;

        if (!likeObj) {
          const response = await axios.get(`http://localhost:8000/api/v1/events/${props.event.id}/likes/`);
          const likes = response.data;
          likeObj = likes.find(like => like.user == userStore.user.id) || null;
        }

        await axios.delete(`http://localhost:8000/api/v1/events/${props.event.id}/likes/${likeObj.id}/`);
        props.event.likes = (props.event.likes || 0) - 1;
        localStorage.removeItem('likeObj');
      }
    };

    const addComment = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login to add comments');
        return;
      }

      if (newComment.value.trim() === '') {
        ElMessage.warning('Please enter a comment');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:8000/api/v1/events/${props.event.id}/comments/`, {
          text: newComment.value
        });
        props.event.comments.push(response.data);
        newComment.value = '';
      } catch (error) {
        ElMessage.error(toErrorText(error, 'Failed to add comment'));
        console.error(error);
      }
    };

    const openTicketPurchaseDialog = () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login to purchase tickets');
        return;
      }

      showTicketPurchaseDialog.value = true;
      selectedTicket.value = null;
    };

    const buyTicket = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login');
        return;
      }

      if (!selectedTicket.value) {
        ElMessage.warning('Please select a ticket');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:8000/api/v1/users/${userStore.user.id}/purchased_tickets/`, {
          event: props.event.id,
          ticket: selectedTicket.value
        });

        ElMessage.success('Ticket purchased successfully');
        showTicketPurchaseDialog.value = false;
        selectedTicket.value = null;
      } catch (error) {
        ElMessage.error(toErrorText(error, 'Failed to purchase ticket'));
        console.error(error);
      }
    };

    return {
      showComments,
      newComment,
      userStore,
      toggleLike,
      addComment,
      showTicketPurchaseDialog,
      selectedTicket,
      openTicketPurchaseDialog,
      buyTicket,
      isSaved,
      toggleSave,
      formattedDate,
      formattedTime
    };
  },
  components: {
    ChatRound,
    Collection,
    CollectionTag,
    HeartIcon
  }
}
</script>

<style scoped>
.event-card :deep(.el-card__body) {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.event-card {
  width: 100%;
  max-width: 600px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  height: 100%;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-content p {
  margin: 0 0 6px;
  line-height: 1.5;
}

.event-extra {
  min-height: 8px;
}

.event-date,
.event-time {
  font-weight: 400;
  color: #303133;
}

.event-category {
  margin-top: 2px;
  color: #303133;
}

.event-title {
  flex: 1;
  min-height: 48px; /* keep header height consistent for multi-line names */
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.saved-icon {
  color: #f56c6c;
}

.category-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}

.category-badge {
  font-size: 12px;
}

.ticket-list {
  margin-top: 16px;
}

.card-footer {
  margin-top: auto;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 12px;
  padding-top: 16px;
  padding-bottom: 12px;
}

.comment-list {
  max-height: 300px;
  overflow-y: auto;
}

.comment-box {
  padding-right: 1%;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-item {
  padding: 12px;
  border-bottom: 1px solid #e4e7ed;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.comment-content {
  font-size: 16px;
}

.ticket-purchase-container {
  padding: 20px;
}

.ticket-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.ticket-price {
  color: #67c23a;
  font-weight: bold;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.purchase-actions {
  margin-top: 20px;
  text-align: right;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}
</style>
