import { createRouter, createWebHistory } from 'vue-router';
import Landing from '../pages/Landing.vue';
import About from '../pages/About.vue';
import Testimonial from '../pages/Testimonial.vue';
import ForecastDashboard from '../pages/ForecastDashboard.vue';
import Pricing from '../pages/Pricing.vue';
import ServicePage from '../pages/ServicePage.vue';
import Login from '../pages/Login.vue';
import Register from '../pages/Register.vue';
import Contact from '../pages/Contact.vue';
// --- ✅ CORRECTED FILE PATH ---
// The filename is case-sensitive in Docker. It should be 'Profile.vue'.
import Profile from '../pages/Profile.vue'; 

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Landing,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/testimonials',
    name: 'Testimonial',
    component: Testimonial,
  },
  {
    path: '/forecast-dashboard',
    name: 'ForecastDashboard',
    component: ForecastDashboard,
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: Pricing,
  },
  {
    path: '/services',
    name: 'ServicePage',
    component: ServicePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
