
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './index.css';
import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();

// Create the Vue application instance and use the router
createApp(App).use(router).mount('#app');
