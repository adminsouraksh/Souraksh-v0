<template>
  <div 
    class="min-h-screen bg-gradient-to-br from-white via-indigo-50 to-purple-50 text-gray-900 font-sans py-12 px-6 relative overflow-hidden"
    @mousemove="updateBlobs"
  >
    <!-- Moving blobs -->
    <div class="absolute w-96 h-96 bg-indigo-200 opacity-40 rounded-full blur-3xl transition-transform duration-300"
      :style="{ transform: `translate(${blob1.x}px, ${blob1.y}px)` }"
    ></div>
    <div class="absolute w-96 h-96 bg-purple-200 opacity-40 rounded-full blur-3xl transition-transform duration-300"
      :style="{ transform: `translate(${blob2.x}px, ${blob2.y}px)` }"
    ></div>

    <div class="container mx-auto relative z-10 animate-fadeIn">
      <h1 class="text-4xl font-bold mb-4 text-indigo-700">{{ service.title }}</h1>
      <p class="text-gray-700 text-lg mb-6">{{ service.details }}</p>
      <router-link 
        to="/services" 
        class="text-indigo-600 hover:underline transition-colors duration-200"
      >← Back to Services</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "ServiceLanding",
  data() {
    return {
      service: {},
      blob1: { x: -200, y: -200 },
      blob2: { x: 200, y: 200 }
    };
  },
  mounted() {
    const serviceId = this.$route.params.id;
    const serviceData = {
      'ai-consulting': { title: 'AI Consulting', details: 'We help businesses leverage Artificial Intelligence for automation, decision-making, and innovation.' },
      'web-dev': { title: 'Web Development', details: 'Modern, responsive websites tailored for your business goals.' },
      'data-analytics': { title: 'Data Analytics', details: 'Extract meaningful insights from your data to drive strategy.' },
      'cloud-solutions': { title: 'Cloud Solutions', details: 'Secure, scalable cloud solutions designed for efficiency.' },
      'automation': { title: 'Automation', details: 'Streamline repetitive processes and boost productivity.' },
      'training': { title: 'Training & Workshops', details: 'Hands-on training programs to upskill your workforce.' }
    };
    this.service = serviceData[serviceId] || { title: 'Service Not Found', details: 'This service does not exist.' };
  },
  methods: {
    updateBlobs(e) {
      this.blob1.x = e.clientX - 400;
      this.blob1.y = e.clientY - 400;
      this.blob2.x = e.clientX + 200;
      this.blob2.y = e.clientY + 200;
    }
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.8s ease-out;
}
</style>
