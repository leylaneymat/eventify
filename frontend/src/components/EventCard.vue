<template>
  <el-card class="event-card">

    <!-- HEADER -->
    <template #header>
      <div class="card-header">
        <h3>{{ event.name }}</h3>

        <div class="header-actions">
          <el-button type="text" @click="toggleLike">
            <el-icon v-if="event.isLiked"><StarFilled /></el-icon>
            <el-icon v-else><Star /></el-icon>
            {{ event.likes || 0 }}
          </el-button>

          <el-button type="text" @click="showComments = true">
            <el-icon><ChatRound /></el-icon>
            {{ event.comments.length || 0 }}
          </el-button>
        </div>
      </div>
    </template>

    <!-- CONTENT -->
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

    <!-- FOOTER -->
    <template #footer>
      <div class="card-footer">
        <el-button type="primary" @click="showPurchase = true">
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
            Add
          </el-button>
        </div>

        <div
          v-for="(comment, idx) in event.comments"
          :key="idx"
          class="comment-item"
        >
          <div class="comment-header">
            <span class="commenter">{{ comment.author }}</span>
            <span class="comment-date">{{ comment.createdAt }}</span>
          </div>
          <div class="comment-content">{{ comment.text }}</div>
        </div>

      </div>
    </el-dialog>

    <!-- PURCHASE DIALOG (UI FINAL VERSION) -->
    <el-dialog v-model="showPurchase" title="Purchase Ticket" width="500px">
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
                :label="`${ticket.name} - $${ticket.price}`"
                :value="ticket.id"
              >
                <div class="ticket-option">
                  <span>{{ ticket.name }}</span>
                  <span class="ticket-price">${{ ticket.price }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <div class="purchase-actions">
          <el-button
            type="primary"
            :disabled="!selectedTicket"
            @click="simulatePurchase"
          >
            Buy
          </el-button>
        </div>

      </div>
    </el-dialog>

  </el-card>
</template>

<script>
import { ref } from "vue";
import { Star, StarFilled, ChatRound } from "@element-plus/icons-vue";

export default {
  props: {
    event: { type: Object, required: true },
  },

  setup(props) {
    /* LIKE BUTTON */
    const toggleLike = () => {
      props.event.isLiked = !props.event.isLiked;
      props.event.likes =
        (props.event.likes || 0) + (props.event.isLiked ? 1 : -1);
    };

    /* COMMENTS */
    const showComments = ref(false);
    const newComment = ref("");

    const addComment = () => {
      if (!newComment.value.trim()) return;

      props.event.comments.push({
        id: Date.now(),
        author: "Guest",
        createdAt: new Date().toLocaleDateString(),
        text: newComment.value,
      });

      newComment.value = "";
    };

    /* PURCHASE UI */
    const showPurchase = ref(false);
    const selectedTicket = ref(null);

    const simulatePurchase = () => {
      alert("Ticket purchased (UI only)");
      showPurchase.value = false;
      selectedTicket.value = null;
    };

    return {
      toggleLike,
      showComments,
      newComment,
      addComment,

      showPurchase,
      selectedTicket,
      simulatePurchase,
    };
  },

  components: { Star, StarFilled, ChatRound },
};
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

/* FOOTER */
.card-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
}

/* COMMENT UI */
.comment-list {
  max-height: 300px;
  overflow-y: auto;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.comment-box {
  width: 80%;
}

.comment-item {
  padding: 12px;
  border-bottom: 1px solid #e4e7ed;
}

.comment-content {
  margin-top: 4px;
  font-size: 15px;
}

/* PURCHASE UI */
.ticket-purchase-container {
  padding: 20px;
}

.ticket-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ticket-price {
  color: #67c23a;
  font-weight: bold;
}

.purchase-actions {
  margin-top: 20px;
  text-align: right;
}
</style>
