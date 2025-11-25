<template>
  <div class="header">
    <div class="header-left">
      <h1 class="app-name">Eventify</h1>
    </div>

    <div class="header-right">
      <el-button type="text" @click="openLoginModal">Login</el-button>
      <el-button type="text" @click="openRegisterModal">Register</el-button>
    </div>
  </div>
  
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
