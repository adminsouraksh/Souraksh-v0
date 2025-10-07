<!-- File: frontend/client/src/components/Footer.vue -->
<template>
  <footer class="bg-gray-900 text-gray-300 py-10">
    <div class="max-w-7xl mx-auto px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-8">
      
      <!-- Brand / About -->
      <div>
      <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">Souraksh</span>
        <p class="text-sm leading-relaxed">
          Building modern solutions with a focus on simplicity and user experience.
        </p>
      </div>

      <!-- Quick Links -->
      <div>
        <h3 class="text-lg font-semibold text-white mb-3">Quick Links</h3>
        <ul class="space-y-2">
          <li><router-link to="/" class="hover:text-white transition">Home</router-link></li>
          <li><router-link to="/about" class="hover:text-white transition">About</router-link></li>
          <li><router-link to="/contact" class="hover:text-white transition">Contact</router-link></li>
          <li><router-link to="/pricing" class="hover:text-white transition">Pricing</router-link></li>
          <li><router-link to="/testimonials" class="hover:text-white transition">Testimonials</router-link></li>
          <li><router-link to="/profile" class="hover:text-white transition">Profile</router-link></li>

        </ul>
      </div>

      <!-- Social Links -->
      <div>
        <h3 class="text-lg font-semibold text-white mb-3">Follow Us</h3>
        <div class="flex space-x-4">
          <a href="#" class="hover:text-white transition" aria-label="Twitter">
            <i class="fab fa-twitter text-2xl"></i>
          </a>
          <a href="#" class="hover:text-white transition" aria-label="Facebook">
            <i class="fab fa-facebook text-2xl"></i>
          </a>
          <a href="#" class="hover:text-white transition" aria-label="Instagram">
            <i class="fab fa-instagram text-2xl"></i>
          </a>
          <a href="#" class="hover:text-white transition" aria-label="LinkedIn">
            <i class="fab fa-linkedin text-2xl"></i>
          </a>
        </div>
      </div>
    </div>

    <!-- Bottom -->
    <div class="mt-10 border-t border-gray-700 pt-6 text-center text-sm text-gray-400">
      © {{ new Date().getFullYear() }} YourBrand. All rights reserved.
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped>
/* Import FontAwesome for icons if not already included */
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
</style>
