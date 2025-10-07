// File: frontend/client/src/main.js

import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';
import './index.css';

// Global state for user authentication
const savedUser = localStorage.getItem('user');
export const globalState = reactive({
  isLoggedIn: !!savedUser,
  user: savedUser ? JSON.parse(savedUser) : null,
});

// Create the Vue application instance and use the router
createApp(App).use(router).mount('#app');
