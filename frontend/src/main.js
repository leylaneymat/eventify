import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { setupAxiosInterceptors, initializeAuth } from './utils/axiosConfig'
import { useUserStore } from './stores/userStore'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router/index.js'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)
app.use(router)

setupAxiosInterceptors()
initializeAuth()

const userStore = useUserStore()
userStore.initializeStore()

await userStore.tryRefreshOnStartup();

app.mount('#app')
