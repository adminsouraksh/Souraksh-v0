<template>
  <div class="min-h-screen font-sans bg-white text-gray-900">
    <!-- Navbar -->
    <Navbar />

    <!-- Hero -->
    <header class="pt-28 pb-16 bg-gradient-to-b from-white to-gray-50 text-center">
      <div class="max-w-3xl mx-auto px-6">
        <h1 class="text-4xl sm:text-5xl font-extrabold leading-tight mb-4">
          What Our <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">Clients Say</span>
        </h1>
        <p class="text-gray-600 max-w-xl mx-auto">
          Real feedback from businesses that trusted Souraksh to transform their forecasting and profitability.
        </p>
      </div>
    </header>

    <!-- Testimonials -->
    <section class="py-20">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Testimonial Card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 hover:shadow-md transition">
            <p class="text-gray-600 mb-6">
              “Souraksh improved our demand accuracy by 90%. We no longer overstock or underdeliver — efficiency at its best.”
            </p>
            <div class="flex items-center gap-4">
              <img
                src="https://randomuser.me/api/portraits/men/45.jpg"
                alt="Client"
                class="w-12 h-12 rounded-full border border-gray-200"
              />
              <div>
                <div class="font-semibold text-gray-900">Rahul Mehta</div>
                <div class="text-sm text-gray-500">Operations Head, RetailCo</div>
              </div>
            </div>
          </div>

          <!-- Testimonial Card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 hover:shadow-md transition">
            <p class="text-gray-600 mb-6">
              “The revenue forecasting insights have been game-changing for us. Our strategic decisions are now data-backed.”
            </p>
            <div class="flex items-center gap-4">
              <img
                src="https://randomuser.me/api/portraits/women/32.jpg"
                alt="Client"
                class="w-12 h-12 rounded-full border border-gray-200"
              />
              <div>
                <div class="font-semibold text-gray-900">Ananya Kapoor</div>
                <div class="text-sm text-gray-500">CFO, TechStart</div>
              </div>
            </div>
          </div>

          <!-- Testimonial Card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 hover:shadow-md transition">
            <p class="text-gray-600 mb-6">
              “The speed of decision-making improved by 60%. We can plan our seasonal campaigns with confidence now.”
            </p>
            <div class="flex items-center gap-4">
              <img
                src="https://randomuser.me/api/portraits/men/78.jpg"
                alt="Client"
                class="w-12 h-12 rounded-full border border-gray-200"
              />
              <div>
                <div class="font-semibold text-gray-900">Vikram Singh</div>
                <div class="text-sm text-gray-500">Marketing Director, FashionHub</div>
              </div>
            </div>
          </div>

          <!-- Testimonial Card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 hover:shadow-md transition">
            <p class="text-gray-600 mb-6">
              “With profitability analysis, we identified 40% cost savings opportunities. Souraksh is a must-have tool.”
            </p>
            <div class="flex items-center gap-4">
              <img
                src="https://randomuser.me/api/portraits/women/65.jpg"
                alt="Client"
                class="w-12 h-12 rounded-full border border-gray-200"
              />
              <div>
                <div class="font-semibold text-gray-900">Neha Sharma</div>
                <div class="text-sm text-gray-500">CEO, GreenFoods</div>
              </div>
            </div>
          </div>

          <!-- Testimonial Card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 hover:shadow-md transition">
            <p class="text-gray-600 mb-6">
              “Integration was seamless, and the customer support team was outstanding. Highly recommend Souraksh.”
            </p>
            <div class="flex items-center gap-4">
              <img
                src="https://randomuser.me/api/portraits/men/12.jpg"
                alt="Client"
                class="w-12 h-12 rounded-full border border-gray-200"
              />
              <div>
                <div class="font-semibold text-gray-900">Arjun Patel</div>
                <div class="text-sm text-gray-500">Founder, LogisticsPro</div>
              </div>
            </div>
          </div>

          <!-- Testimonial Card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 hover:shadow-md transition">
            <p class="text-gray-600 mb-6">
              “Our planning cycle shrunk from weeks to days. The insights are accurate and easy to interpret.”
            </p>
            <div class="flex items-center gap-4">
              <img
                src="https://randomuser.me/api/portraits/women/90.jpg"
                alt="Client"
                class="w-12 h-12 rounded-full border border-gray-200"
              />
              <div>
                <div class="font-semibold text-gray-900">Priya Nair</div>
                <div class="text-sm text-gray-500">Head of Strategy, FinEdge</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-indigo-700 text-white text-center">
      <div class="max-w-4xl mx-auto px-6">
        <h3 class="text-2xl font-semibold mb-3">Join our growing list of happy clients</h3>
        <p class="mb-6 text-indigo-100">Experience the power of accurate forecasting and profitability planning with Souraksh.</p>
        <router-link
          to="/register"
          class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-white text-indigo-700 font-semibold hover:bg-indigo-50 transition"
        >
          Get Started Today
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

.font-sans {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
}
</style>
