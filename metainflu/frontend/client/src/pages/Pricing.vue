<template>
  <div class="min-h-screen font-sans bg-white text-gray-900">
    <!-- Navbar -->
    <Navbar />

    <!-- Hero -->
    <header class="pt-28 pb-16 bg-gradient-to-b from-white to-gray-50 text-center">
      <div class="max-w-3xl mx-auto px-6">
        <h1 class="text-4xl sm:text-5xl font-extrabold leading-tight mb-4">
          Simple <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">Pricing</span> for Every Business
        </h1>
        <p class="text-gray-600 max-w-xl mx-auto">
          Choose a plan that fits your needs. No hidden fees, no long-term contracts.
        </p>
      </div>
    </header>

    <!-- Pricing Plans -->
    <section class="py-20">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Basic Plan -->
          <div class="p-8 bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md transition">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Starter</h3>
            <p class="text-gray-600 text-sm mb-6">Perfect for small teams and startups.</p>
            <div class="text-4xl font-extrabold text-indigo-600 mb-2">$19<span class="text-lg font-medium text-gray-500">/mo</span></div>
            <ul class="text-gray-600 text-sm space-y-3 mb-6">
              <li>✔ Basic demand forecasting</li>
              <li>✔ Revenue trend reports</li>
              <li>✔ Email support</li>
              <li>✘ Advanced analytics</li>
            </ul>
            <router-link
              to="/register"
              class="block w-full text-center py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition"
            >
              Get Started
            </router-link>
          </div>

          <!-- Pro Plan -->
          <div class="p-8 bg-indigo-700 text-white rounded-2xl shadow-lg relative">
            <span class="absolute top-4 right-4 text-xs font-semibold bg-white text-indigo-700 px-3 py-1 rounded-full">Most Popular</span>
            <h3 class="text-lg font-semibold mb-2">Professional</h3>
            <p class="text-indigo-100 text-sm mb-6">Best for growing businesses and enterprises.</p>
            <div class="text-4xl font-extrabold mb-2">$49<span class="text-lg font-medium text-indigo-200">/mo</span></div>
            <ul class="text-indigo-100 text-sm space-y-3 mb-6">
              <li>✔ Advanced demand forecasting</li>
              <li>✔ Revenue & profit estimation</li>
              <li>✔ Priority email & chat support</li>
              <li>✔ Custom dashboards</li>
            </ul>
            <router-link
              to="/register"
              class="block w-full text-center py-3 rounded-lg bg-white text-indigo-700 font-semibold hover:bg-gray-100 transition"
            >
              Start Free Trial
            </router-link>
          </div>

          <!-- Enterprise Plan -->
          <div class="p-8 bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md transition">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Enterprise</h3>
            <p class="text-gray-600 text-sm mb-6">Tailored for large corporations with advanced needs.</p>
            <div class="text-4xl font-extrabold text-indigo-600 mb-2">Custom</div>
            <ul class="text-gray-600 text-sm space-y-3 mb-6">
              <li>✔ All Pro features</li>
              <li>✔ Dedicated account manager</li>
              <li>✔ 24/7 priority support</li>
              <li>✔ Custom integrations</li>
            </ul>
            <router-link
              to="/contact"
              class="block w-full text-center py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition"
            >
              Contact Sales
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-gray-50 text-center">
      <div class="max-w-4xl mx-auto px-6">
        <h3 class="text-2xl font-semibold mb-3">Not sure which plan is right for you?</h3>
        <p class="mb-6 text-gray-600">Book a demo and we’ll help you find the best fit for your business.</p>
        <router-link
          to="/demo"
          class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition"
        >
          Book a Demo
        </router-link>
      </div>
    </section>

    <!-- Footer -->
  <Footer />

  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
}
</style>
