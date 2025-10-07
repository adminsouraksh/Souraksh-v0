<!-- File: frontend/client/src/pages/About.vue -->
<template>
  <div class="min-h-screen font-sans bg-white text-gray-900">
    <!-- Navbar -->
    <Navbar />

    <!-- Hero -->
    <header class="pt-28 pb-16 bg-gradient-to-b from-white to-gray-50">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight">
          About <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">Souraksh</span>
        </h1>
        <p class="text-gray-600 max-w-2xl mx-auto mt-6">
          We are on a mission to make forecasting simple, reliable, and actionable.  
          Our platform empowers businesses with the tools to plan smarter and grow confidently.
        </p>
      </div>
    </header>

    <!-- Mission -->
    <section class="py-20">
      <div class="max-w-5xl mx-auto px-6 text-center">
        <div class="p-10 bg-white rounded-3xl shadow-sm border border-gray-100">
          <h2 class="text-3xl font-bold mb-4">Our Mission</h2>
          <p class="text-gray-600 leading-relaxed">
            At Souraksh, we believe in transforming complex data into clear insights.  
            Our mission is to help organizations forecast demand, estimate revenue,  
            and maximize profitability with speed, accuracy, and confidence.
          </p>
        </div>
      </div>
    </section>

    <!-- Values -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-3xl font-bold text-center mb-12">Our Core Values</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="service-card text-center">
            <div class="icon">🤝</div>
            <h3 class="font-semibold text-lg">Collaboration</h3>
            <p class="text-gray-600 text-sm">We work hand-in-hand with businesses to create lasting impact.</p>
          </div>
          <div class="service-card text-center">
            <div class="icon">⚡</div>
            <h3 class="font-semibold text-lg">Innovation</h3>
            <p class="text-gray-600 text-sm">We innovate constantly to deliver smarter forecasting solutions.</p>
          </div>
          <div class="service-card text-center">
            <div class="icon">🌍</div>
            <h3 class="font-semibold text-lg">Impact</h3>
            <p class="text-gray-600 text-sm">We measure success by the tangible results our clients achieve.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <h2 class="text-2xl font-bold mb-6">Souraksh in Numbers</h2>
        <p class="text-gray-600 mb-8">Proven results and growing community.</p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="stat-card">
            <div class="stat-value">95%</div>
            <div class="text-xs text-gray-500">Accuracy Achieved</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">70%</div>
            <div class="text-xs text-gray-500">Faster Planning</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">500+</div>
            <div class="text-xs text-gray-500">Global Clients</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">40%</div>
            <div class="text-xs text-gray-500">Cost Reduction</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <h3 class="text-2xl font-semibold mb-3">Want to know more about us?</h3>
        <p class="mb-6 text-indigo-100 max-w-2xl mx-auto">
          Discover how Souraksh is redefining forecasting and planning.  
          Partner with us and unlock the future of data-driven growth.
        </p>
        <router-link
          to="/contact"
          class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-white text-indigo-700 font-semibold hover:bg-gray-100 transition"
        >
          Contact Us
        </router-link>
      </div>
    </section>

    <!-- Footer -->
   <Footer/>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

:root {
  --accent-1: #5b21b6; /* indigo-600 */
  --accent-2: #7c3aed; /* purple-600 */
}

.font-sans {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
}

.service-card {
  background: white;
  padding: 18px;
  border-radius: 14px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 1px 4px rgba(16, 24, 40, 0.03);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.service-card .icon {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stat-card {
  background: white;
  padding: 18px;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}
.stat-value {
  font-weight: 700;
  font-size: 22px;
  color: var(--accent-1);
}
</style>
