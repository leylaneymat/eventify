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
</template>

<script setup>
import { ref } from 'vue'

const loginDialogVisible = ref(false)
const registerDialogVisible = ref(false)

const openLoginModal = () => loginDialogVisible.value = true
const openRegisterModal = () => registerDialogVisible.value = true
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
