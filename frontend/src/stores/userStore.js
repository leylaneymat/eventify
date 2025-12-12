import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
	state: () => ({
		user: null,
		isLoggedIn: false,
		accessToken: null,
		refreshToken: null,
		savedEvents: [],
		savedEventsLoaded: false,
	}),
	actions: {
		async login(username, password) {
			try {
				const response = await axios.post(
					"http://localhost:8000/api/v1/token/",
					{
						username,
						password,
					},
				);

				this.accessToken = response.data.access;
				this.refreshToken = response.data.refresh;

				axios.defaults.headers.common["Authorization"] =
					`Bearer ${this.accessToken}`;

				const userData = (
					await axios.get(
						`http://localhost:8000/api/v1/users/${username}/`,
					)
				).data;

				this.user = {
					id: userData.id,
					username: userData.username,
				};
				this.isLoggedIn = true;

				localStorage.setItem("user", JSON.stringify(this.user));
				localStorage.setItem("accessToken", this.accessToken);
				localStorage.setItem("refreshToken", this.refreshToken);
				localStorage.setItem("isLoggedIn", this.isLoggedIn);

				// Load saved events after login
				await this.loadSavedEvents();

				return true;
			} catch (error) {
				console.error("Login failed", error);
				return false;
			}
		},

		async register(username, password) {
			try {
				await axios.post("http://localhost:8000/api/v1/users/", {
					username,
					password,
				});

				return await this.login(username, password);
			} catch (error) {
				console.error("Registration failed", error);
				return false;
			}
		},

		async refresh() {
			try {
				const response = await axios.post(
					"http://localhost:8000/api/v1/token/refresh/",
					{
						refresh: this.refreshToken,
					},
				);

				this.accessToken = response.data.access;

				axios.defaults.headers.common["Authorization"] =
					`Bearer ${this.accessToken}`;
				localStorage.setItem("accessToken", this.accessToken);
				return true;
			} catch (error) {
				this.logout();
				return false;
			}
		},

		logout() {
			this.user = null;
			this.isLoggedIn = false;
			this.accessToken = null;
			this.refreshToken = null;
			this.savedEvents = [];
			this.savedEventsLoaded = false;

			delete axios.defaults.headers.common["Authorization"];

			localStorage.removeItem("user");
			localStorage.removeItem("accessToken");
			localStorage.removeItem("refreshToken");
			localStorage.removeItem("isLoggedIn");
		},

		initializeStore() {
			this.user = JSON.parse(localStorage.getItem("user"));
			this.accessToken = localStorage.getItem("accessToken");
			this.refreshToken = localStorage.getItem("refreshToken");
			this.isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

			if (this.accessToken && this.refreshToken) {
				axios.defaults.headers.common["Authorization"] =
					`Bearer ${this.accessToken}`;

				// Load saved events if user is logged in
				if (this.isLoggedIn) {
					this.loadSavedEvents();
				}
			}
		},

		async tryRefreshOnStartup() {
			const refreshToken = localStorage.getItem("refreshToken");
		  
			if (!refreshToken) {
			  this.logout();
			  return;
			}
		  
			try {
			  const response = await axios.post(
				"http://localhost:8000/api/v1/token/refresh/",
				{
				  refresh: refreshToken,
				}
			  );
		  
			  this.accessToken = response.data.access;
			  this.isLoggedIn = true;
		  
			  axios.defaults.headers.common["Authorization"] =
				`Bearer ${this.accessToken}`;
		  
			  localStorage.setItem("accessToken", this.accessToken);
			} catch (error) {
			  this.logout();
			}
		  },
		  

		// Saved Events Actions
		async loadSavedEvents() {
			if (!this.isLoggedIn) return;

			try {
				const response = await axios.get(
					"http://localhost:8000/api/v1/events/saved/",
				);
				this.savedEvents = response.data;
				this.savedEventsLoaded = true;
			} catch (error) {
				console.error("Failed to load saved events", error);
				this.savedEvents = [];
			}
		},

		async saveEvent(eventId) {
			if (!this.isLoggedIn) {
				throw new Error("User not logged in");
			}

			try {
				const response = await axios.post(
					"http://localhost:8000/api/v1/events/saved/save/",
					{ event_id: eventId },
				);

				// Add to local state
				this.savedEvents.push(response.data);
				return true;
			} catch (error) {
				console.error("Failed to save event", error);
				throw error;
			}
		},

		async unsaveEvent(eventId) {
			if (!this.isLoggedIn) {
				throw new Error("User not logged in");
			}

			try {
				await axios.delete(
					`http://localhost:8000/api/v1/events/saved/${eventId}/`,
				);

				// Remove from local state
				this.savedEvents = this.savedEvents.filter(
					(saved) => saved.event.id !== eventId,
				);
				return true;
			} catch (error) {
				console.error("Failed to unsave event", error);
				throw error;
			}
		},

		async checkEventSaved(eventId) {
			if (!this.isLoggedIn) return false;

			try {
				const response = await axios.get(
					`http://localhost:8000/api/v1/events/saved/check/${eventId}/`,
				);
				return response.data.is_saved;
			} catch (error) {
				console.error("Failed to check saved status", error);
				return false;
			}
		},
	},
});
