import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
	state: () => ({
		user: null,
		isLoggedIn: false,
		accessToken: null,
		refreshToken: null,
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
			}
		},
	},
});
