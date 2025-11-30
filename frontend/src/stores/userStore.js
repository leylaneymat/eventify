import { defineStore } from "pinia"

export const useUserStore = defineStore("user", {
  state: () => ({
    isLoggedIn: false,
    user: null
  }),
  actions: {
    initializeStore() {
      const storedUser = localStorage.getItem("user")
      if (storedUser) {
        this.user = JSON.parse(storedUser)
        this.isLoggedIn = true
      }
    },
    setUser(user) {
      this.user = user
      this.isLoggedIn = true
      localStorage.setItem("user", JSON.stringify(user))
    }
  }
})
