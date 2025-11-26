<template>
  <div class="header">
    <div class="header-left">
      <h1 class="app-name">Eventify</h1>
    </div>

    <div class="header-right">
      <template v-if="userStore.isLoggedIn">
        <el-button type="text" @click="showPurchased">Purchased tickets</el-button>
        |
        <span>{{ userStore.user?.username }}</span>
        <el-button type="text" @click="userStore.logout">Logout</el-button>
      </template>
      <template v-else>
        <el-button type="text" @click="openLoginModal">Login</el-button>
        <el-button type="text" @click="openRegisterModal">Register</el-button>
      </template>
    </div>
  
  <el-dialog v-model="purchasedTicketsDialogVisible" title="Purchased Tickets" width="700px">
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading">
          <Loading />
        </el-icon>
        <p>Loading tickets...</p>
      </div>
      <div v-else-if="purchasedTickets.length === 0" class="no-tickets">
        <p>You haven't purchased any tickets yet.</p>
      </div>
      <el-table v-else :data="purchasedTickets" style="width: 100%">
        <el-table-column label="Event Name" prop="event.name" width="200" />
        <el-table-column label="Ticket Name" prop="ticket.name" width="150" />
        <el-table-column label="Price" width="100">
          <template #default="scope">
            ${{ scope.row.ticket.price }}
          </template>
        </el-table-column>
        <el-table-column label="Purchase Date" pro width="200">
          <template #default="scope">
            {{ scope.row.purchaseDate }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

  <el-dialog v-model="loginDialogVisible" title="Login" width="500px">
  <el-form :model="loginForm">
    <el-form-item label="Username">
      <el-input v-model="loginForm.username" />
    </el-form-item>
    <el-form-item label="Password">
      <el-input v-model="loginForm.password" type="password" />
    </el-form-item>
    <el-button type="primary">Login</el-button>
  </el-form>
</el-dialog>

<el-dialog v-model="registerDialogVisible" title="Register" width="500px">
  <el-form :model="registerForm">
    <el-form-item label="Username">
      <el-input v-model="registerForm.username" />
    </el-form-item>
    <el-form-item label="Password">
      <el-input v-model="registerForm.password" type="password" />
    </el-form-item>
  </el-form>
</el-dialog>

</div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

const loginDialogVisible = ref(false)
const registerDialogVisible = ref(false)

const openLoginModal = () => loginDialogVisible.value = true
const openRegisterModal = () => registerDialogVisible.value = true

const submitLogin = async () => {
  const success = await userStore.login(loginForm.value.username, loginForm.value.password)
  if (success) {
    ElMessage.success('Login successful')
    loginDialogVisible.value = false
  } else {
    ElMessage.error('Login failed')
  }
}

const purchasedTicketsDialogVisible = ref(false)
const purchasedTickets = ref([])
const loading = ref(false)

const showPurchased = async () => {
  purchasedTicketsDialogVisible.value = true
  loading.value = true
  const result = await axios.get(`http://localhost:8000/api/v1/users/${userStore.user.id}/purchased_tickets/`)
  purchasedTickets.value = result.data
  loading.value = false
}

</script>

<style scoped>
.header {
  background-color: #409eff;
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
}
</style>
