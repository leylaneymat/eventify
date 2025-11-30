<template>
    <footer class="w-full py-6 border-t border-gray-200 bg-white dark:bg-gray-900">
      <div class="mx-auto max-w-7xl px-4 text-center text-sm text-gray-600 dark:text-gray-300">
        <span>Made with</span>
        <span class="mx-1">❤️</span>
        <a
          href="https://github.com/leylaneymat"
          target="_blank"
          class="font-medium hover:underline text-blue-600 dark:text-blue-400"
        >
          Team 10
        </a>
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