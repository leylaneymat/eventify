<template>
  <footer class="custom-footer">
    <div class="footer-content">
      Made with
      <span class="heart">❤️</span>
      by <a class="link" href="https://github.com/leylaneymat/eventify">Team 10</a>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.custom-footer {
  background-color: #2c3e50;
  color: white;
  padding: 16px 24px;
  text-align: center;
  position: relative;
  z-index: 1;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.link {
  color: #ffffff;
  text-decoration: none;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  font-size: 14px;
}

.heart {
  color: #ff4757;
  animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}
</style>