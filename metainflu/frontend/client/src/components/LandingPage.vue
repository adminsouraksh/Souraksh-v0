<template>
  <div class="relative min-h-screen bg-gradient-to-b from-blue-900 to-blue-800 text-white overflow-hidden">
    <!-- Light blob behind hero text -->
    <div
      class="absolute w-96 h-96 bg-blue-500 rounded-full opacity-40 blur-3xl transition-transform duration-300 ease-out"
      :style="{ transform: `translate(${cursor.x}px, ${cursor.y}px)` }"
    ></div>

    <!-- Hero Section -->
    <section class="relative z-10 flex flex-col items-center justify-center h-screen text-center px-6">
      <h1
        ref="scrambleText"
        class="text-6xl font-bold mb-4"
      >
        METABERRY
      </h1>
      <p class="text-lg mb-6">Leading the way in consulting, marketing & freelance services</p>
      <button class="px-6 py-3 bg-blue-600 rounded-lg hover:bg-blue-700 transition">
        Get Started
      </button>
    </section>

    <!-- Services Section -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6 px-6 pb-20 text-center">
      <div v-for="(service, i) in services" :key="i"
           class="p-6 bg-blue-700 bg-opacity-50 rounded-xl hover:scale-105 transition-transform duration-300">
        <h3 class="text-xl font-semibold mb-2">{{ service.title }}</h3>
        <p>{{ service.desc }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const cursor = ref({ x: 0, y: 0 });
const services = [
  { title: 'Strategy', desc: 'Helping you plan for success.' },
  { title: 'Digital Transformation', desc: 'Adapting businesses for the future.' },
  { title: 'Analytics', desc: 'Data-driven decision making.' },
];

// Move light blob with cursor
window.addEventListener('mousemove', (e) => {
  cursor.value = { x: e.clientX - 200, y: e.clientY - 200 };
});

// Text scramble animation
const scrambleText = ref(null);
onMounted(() => {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let interval = null;
  let iteration = 0;
  const original = scrambleText.value.innerText;

  interval = setInterval(() => {
    scrambleText.value.innerText = original
      .split("")
      .map((letter, idx) => {
        if (idx < iteration) return original[idx];
        return letters[Math.floor(Math.random() * 26)];
      })
      .join("");

    if (iteration >= original.length) clearInterval(interval);
    iteration += 1 / 3;
  }, 50);
});
</script>

<style scoped>
section {
  transition: all 0.5s ease-in-out;
}
</style>
