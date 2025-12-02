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
      <el-form :model="loginForm" label-width="120px">
        <el-form-item label="Username">
          <el-input v-model="loginForm.username" placeholder="Enter your username" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="loginForm.password" type="password" placeholder="Enter your password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitLogin">Login</el-button>
          <el-button class="cancel-button" @click="loginDialogVisible = false">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog v-model="registerDialogVisible" title="Register" width="500px">
      <el-form :model="registerForm" label-width="120px">
        <el-form-item label="Username">
          <el-input v-model="registerForm.username" placeholder="Choose a username" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="registerForm.password" type="password" placeholder="Create a password" show-password />
        </el-form-item>
        <el-form-item label="Confirm">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="Confirm your password"
            show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitRegister">Register</el-button>
          <el-button class="cancel-button" @click="registerDialogVisible = false">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

</div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { ElMessage } from 'element-plus'
import axios from 'axios';

const userStore = useUserStore()

const loginDialogVisible = ref(false)
const registerDialogVisible = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const openLoginModal = () => {
  loginDialogVisible.value = true
}

const openRegisterModal = () => {
  registerDialogVisible.value = true
}

const submitLogin = async () => {
  const { username, password } = loginForm.value

  if (!username || !password) {
    ElMessage.error('Please enter username and password')
    return
  }

  const success = await userStore.login(username, password)

  if (success) {
    ElMessage.success('Login successful')
    loginDialogVisible.value = false
  } else {
    ElMessage.error('Login failed')
  }
}

const submitRegister = async () => {
  const { username, password, confirmPassword } = registerForm.value

  if (!username || !password) {
    ElMessage.error('Please enter username and password')
    return
  }

  if (password !== confirmPassword) {
    ElMessage.error('Passwords do not match')
    return
  }

  const success = await userStore.register(username, password)

  if (success) {
    ElMessage.success('Registration successful')
    registerDialogVisible.value = false
  } else {
    ElMessage.error('Registration failed')
  }
}

const purchasedTicketsDialogVisible = ref(false)
const purchasedTickets = ref([])
const loading = ref(false)

const showPurchased = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('Please login first')
    return
  }

  purchasedTickets.value = []
  purchasedTicketsDialogVisible.value = true
  loading.value = true

  try {
    const purchased_tickets = (await axios.get(`http://localhost:8000/users/${userStore.user.id}/purchased_tickets/`)).data

    for (let i = 0; i < purchased_tickets.length; i++) {
      const selected_event = (await axios.get(`http://localhost:8000/events/${purchased_tickets[i].event}/`)).data
      const selected_ticket = (await axios.get(`http://localhost:8000/events/${purchased_tickets[i].event}/tickets/${purchased_tickets[i].ticket}/`)).data
      purchasedTickets.value.push({
        'id': purchased_tickets[i].id,
        'purchaseDate': purchased_tickets[i].purchase_date,
        'event': {
          'id': selected_event.id,
          'name': selected_event.name
        },
        'ticket': {
          'id': selected_ticket.id,
          'name': selected_ticket.name,
          'price': selected_ticket.price
        }
      })
    }
  } catch (error) {
    ElMessage.error('Failed to load purchased tickets')
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.header-left {
  display: flex;
  align-items: center;
}

.app-name {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  column-gap: 16px;
}

.el-button {
  color: white;
}

.cancel-button {
  color: black;
}
</style>
