<template>
  <div class="min-h-screen font-sans bg-gray-50 text-gray-900">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <main class="pt-24 pb-16">
      <div class="max-w-2xl mx-auto px-6">
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-8">
          <div class="flex flex-col items-center text-center">
            <!-- Profile Picture -->
            <img 
              :src="userProfile.picture || 'https://placehold.co/128x128/e2e8f0/64748b?text=User'" 
              alt="User profile picture"
              class="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg mb-4"
            >

            <!-- User Name -->
            <h1 class="text-3xl font-bold text-gray-800">{{ userProfile.name }}</h1>
            
            <!-- User Email -->
            <p class="text-gray-500 mt-1">{{ userProfile.email }}</p>

            <!-- Sign-in Method Badge -->
            <div class="mt-4">
              <span v-if="userProfile.signInMethod === 'google'" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                <i class="fab fa-google mr-2"></i> Signed in with Google
              </span>
              <span v-else class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                <i class="fas fa-envelope mr-2"></i> Signed in with Email
              </span>
            </div>
          </div>

          <!-- Divider -->
          <hr class="my-8 border-gray-200">

          <!-- Actions -->
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="w-full inline-flex items-center justify-center px-6 py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition">
              <i class="fas fa-edit mr-2"></i> Edit Profile
            </button>
            <button @click="logout" class="w-full inline-flex items-center justify-center px-6 py-3 rounded-lg bg-gray-100 text-gray-700 font-semibold hover:bg-gray-200 transition">
              Log Out
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import { globalState } from '../main.js';

const router = useRouter();

// Create a computed property for the user profile to ensure reactivity
const userProfile = computed(() => {
  if (globalState.user) {
    return {
      name: globalState.user.name,
      email: globalState.user.email,
      // The picture might be available if the user signed in with Google
      picture: globalState.user.picture, 
      // Determine sign-in method based on the presence of googleId
      signInMethod: globalState.user.googleId ? 'google' : 'email'
    };
  }
  // Return a default object if the user is not logged in
  return {
    name: 'Guest',
    email: 'No user logged in',
    picture: null,
    signInMethod: 'none'
  };
});

const logout = () => {
  localStorage.removeItem('user');
  globalState.isLoggedIn = false;
  globalState.user = null;
  router.push('/login');
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
</style>
