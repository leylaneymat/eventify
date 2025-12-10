import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/Homeview.vue";
import SavedEventsView from "../views/SavedEventsView.vue";

const routes = [
	{
		path: "/",
		name: "home",
		component: HomeView,
	},
	{
		path: "/saved",
		name: "saved-events",
		component: SavedEventsView,
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
