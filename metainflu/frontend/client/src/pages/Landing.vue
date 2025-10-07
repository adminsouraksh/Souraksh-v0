<template>
  <div class="min-h-screen font-sans bg-white text-gray-900">
    <!-- Navbar -->
    <Navbar />

    <!-- Hero -->
    <header class="pt-28 pb-16 bg-gradient-to-b from-white to-gray-50">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="space-y-6">
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight">
              AI-Powered  <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">Forecasting</span> for Smarter Business Decisions
            </h1>
            <p class="text-gray-600 max-w-xl">
              Turn your sales data into actionable forecasts, insights, and revenue projections.
            </p>

            <div class="flex flex-col sm:flex-row gap-4 mt-4">
              <router-link
                to="/demo"
                class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold hover:from-blue-600 hover:to-purple-600 transition-shadow shadow-sm"
              >
                Request a Demo
              </router-link>

              <router-link
                to="/services"
                class="inline-flex items-center justify-center px-6 py-3 rounded-lg border border-gray-200 text-gray-800 hover:bg-gray-100 transition"
              >
                Learn More
              </router-link>
            </div>

            <div class="mt-6 flex items-center gap-6 text-sm text-gray-500">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-indigo-50 flex items-center justify-center">📈</div>
                <div>
                  <div class="font-semibold text-gray-900">95%</div>
                  <div class="text-xs">Forecast Accuracy</div>
                </div>
              </div>

              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-indigo-50 flex items-center justify-center">⚡</div>
                <div>
                  <div class="font-semibold text-gray-900">Faster Decisions</div>
                  <div class="text-xs">Reduce planning time by up to 70%</div>
                </div>
              </div>
            </div>
          </div>

          <div class="relative">
            <div class="mx-auto max-w-md lg:max-w-lg bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <div class="text-xs text-gray-500">ForecastX</div>
                  <div class="font-semibold">Monthly Demand Overview</div>
                </div>
                <div class="text-sm text-gray-500">Oct 2025</div>
              </div>

              <div class="h-44 rounded-lg bg-gradient-to-tr from-indigo-50 to-white flex items-end p-4">
                <!-- minimal placeholder chart bars -->
                <div class="w-full flex items-end gap-2">
                  <div class="flex-1 h-16 rounded-md bg-indigo-600/80"></div>
                  <div class="flex-1 h-10 rounded-md bg-indigo-400/80"></div>
                  <div class="flex-1 h-20 rounded-md bg-indigo-600/60"></div>
                  <div class="flex-1 h-8 rounded-md bg-indigo-300/80"></div>
                  <div class="flex-1 h-24 rounded-md bg-indigo-700/80"></div>
                </div>
              </div>

              <div class="mt-4 text-sm text-gray-600">Projected demand increases during seasonal peak. Inventory suggestions available.</div>
            </div>

            <div class="hidden lg:block absolute -right-10 -bottom-10 w-64 h-64 rounded-3xl bg-gradient-to-tr from-indigo-100 to-purple-50 transform rotate-12 blur-xl opacity-60"></div>
          </div>
        </div>
      </div>
    </header>

    <!-- Services -->
    <section class="py-20">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-3xl font-bold text-center mb-10">Our Services</h2>
        <p class="text-center text-gray-600 max-w-2xl mx-auto mb-8">Data-driven forecasting and financial insights tailored to your business.</p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="service-card">
            <div class="icon">📊</div>
            <h3 class="font-semibold text-lg">Demand Forecasting</h3>
            <p class="text-gray-600 text-sm">Predict product demand accurately to optimize inventory and operations.</p>
          </div>

          <div class="service-card">
            <div class="icon">💵</div>
            <h3 class="font-semibold text-lg">Revenue Estimation</h3>
            <p class="text-gray-600 text-sm">Forecast revenue trends and inform strategic planning.</p>
          </div>

          <div class="service-card">
            <div class="icon">📈</div>
            <h3 class="font-semibold text-lg">Profitability Analysis</h3>
            <p class="text-gray-600 text-sm">Analyze costs and margins to maximize profitability.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Products -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-3xl font-bold">Products</h2>
          <router-link to="/products" class="text-sm text-indigo-600 font-semibold">View all products →</router-link>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-6 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
            <div class="text-sm text-gray-500 mb-2">ForecastX</div>
            <div class="font-semibold mb-2">AI demand engine</div>
            <p class="text-gray-600 text-sm">Accurate demand predictions for retail and supply chain.</p>
          </div>

          <div class="p-6 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
            <div class="text-sm text-gray-500 mb-2">RevenueVision</div>
            <div class="font-semibold mb-2">Revenue & trend forecasting</div>
            <p class="text-gray-600 text-sm">Predict revenue patterns and optimize growth strategies.</p>
          </div>

          <div class="p-6 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
            <div class="text-sm text-gray-500 mb-2">ProfitTrack</div>
            <div class="font-semibold mb-2">Profit estimation toolkit</div>
            <p class="text-gray-600 text-sm">Track and estimate profitability with actionable insights.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Impact / Stats -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <h2 class="text-2xl font-bold mb-6">Our Impact</h2>
        <p class="text-gray-600 mb-8">Tangible results from forecasting and financial planning.</p>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="stat-card">
            <div class="stat-value">95%</div>
            <div class="text-xs text-gray-500">Forecast Accuracy</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">70%</div>
            <div class="text-xs text-gray-500">Faster Decisions</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">500+</div>
            <div class="text-xs text-gray-500">Clients Served</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">40%</div>
            <div class="text-xs text-gray-500">Cost Optimization</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <h3 class="text-2xl font-semibold mb-3">Ready to plan with confidence?</h3>
        <p class="mb-6 text-indigo-100 max-w-2xl mx-auto">Book a demo and we’ll show how Souraksh can transform your planning and profitability.</p>
        <router-link to="/demo" class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-white text-indigo-700 font-semibold">Book a Demo</router-link>
      </div>
    </section>
<Footer />
    <!-- Footer -->
  
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

:root{
  --accent-1: #5b21b6; /* indigo-600 */
  --accent-2: #7c3aed; /* purple-600 */
}

*{box-sizing:border-box}

.font-sans{font-family:'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial}

.text-gradient{
  background: linear-gradient(90deg,var(--accent-1),var(--accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.service-card{
  background:white;
  padding:18px;
  border-radius:14px;
  border:1px solid #f1f5f9;
  box-shadow:0 1px 4px rgba(16,24,40,0.03);
  display:flex;
  flex-direction:column;
  gap:10px;
}
.service-card .icon{width:46px;height:46px;border-radius:10px;background:#f8fafc;display:flex;align-items:center;justify-content:center;font-size:20px}

.stat-card{
  background:white;
  padding:18px;
  border-radius:12px;
  border:1px solid #f1f5f9;
}
.stat-value{font-weight:700;font-size:22px;color:var(--accent-1)}

/* responsive tweaks */
@media (min-width:1024px){
  header{padding-top:4rem}
}
</style>