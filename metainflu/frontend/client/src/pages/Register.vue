<!-- File: frontend/client/src/pages/Register.vue -->
<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <router-link to="/" class="text-3xl font-extrabold text-indigo-600 tracking-tight">
          Souraksh
        </router-link>
        <h2 class="mt-4 text-2xl font-bold text-gray-900">
          Create your account
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Get started with your 30-day free trial.
        </p>
      </div>

      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <div>
            <label for="full-name" class="sr-only">Full Name</label>
            <input
              id="full-name"
              v-model="name"
              type="text"
              placeholder="Full Name"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 sm:text-sm"
              required
            />
          </div>

          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input
              id="email-address"
              v-model="email"
              type="email"
              placeholder="Email Address"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 sm:text-sm"
              required
            />
          </div>

          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Password"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 sm:text-sm"
              required
            />
          </div>

          <div v-if="errorMessage" class="text-red-600 text-sm">
            {{ errorMessage }}
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-70"
            >
              <span v-if="loading">Creating Account...</span>
              <span v-else>Create Account</span>
            </button>
          </div>
        </form>

        <div class="my-6 flex items-center">
          <div class="flex-grow border-t border-gray-200"></div>
          <span class="mx-4 text-xs font-medium text-gray-500 uppercase">Or</span>
          <div class="flex-grow border-t border-gray-200"></div>
        </div>
        
        <div id="google-signin-button-container-register" class="flex justify-center"></div>

      </div>

      <p class="text-center text-sm text-gray-600">
        Already have an account?
        <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
          Sign in
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/authService';
import { globalState } from '../main.js';

export default {
  name: 'Register',
  setup() {
    const router = useRouter();
    const name = ref('');
    const email = ref('');
    const password = ref('');
    const loading = ref(false);
    const errorMessage = ref('');

    const handleRegister = async () => {
      loading.value = true;
      errorMessage.value = '';
      try {
        const userData = {
          name: name.value,
          email: email.value,
          password: password.value,
        };
        const response = await authService.register(userData);
        globalState.isLoggedIn = true;
        globalState.user = response;
        router.push('/forecast-dashboard');
      } catch (error) {
        errorMessage.value = error.message || 'Registration failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    const handleGoogleLogin = async (googleResponse) => {
        try {
            const response = await authService.loginWithGoogle(googleResponse.credential);
            globalState.isLoggedIn = true;
            globalState.user = response;
            router.push('/forecast-dashboard');
        } catch(error) {
            errorMessage.value = error.message || 'Google Sign-Up failed. Please try again.';
            console.error("Google login failed:", error);
        }
    };

    const loadGoogleScript = () => {
      if (document.getElementById('google-identity-script')) {
        if (typeof google !== 'undefined') {
          initializeGoogleSignIn();
        }
        return;
      }

      const script = document.createElement('script');
      script.id = 'google-identity-script';
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.onload = initializeGoogleSignIn;
      document.head.appendChild(script);
    };

    const initializeGoogleSignIn = () => {
      try {
        if (typeof google !== 'undefined') {
            google.accounts.id.initialize({
                client_id: document.querySelector('meta[name="google-signin-client_id"]').content,
                callback: handleGoogleLogin,
            });
            google.accounts.id.renderButton(
                document.getElementById('google-signin-button-container-register'),
                { theme: 'outline', size: 'large', type: 'standard', text: 'signup_with', width: '300' }
            );
        } else {
             console.error("Google object not found after script load.");
             errorMessage.value = "Could not initialize Google Sign-In. Please try again.";
        }
      } catch (error) {
        console.error("Error initializing Google Sign-In:", error);
        errorMessage.value = "An error occurred with Google Sign-In.";
      }
    };

    onMounted(() => {
        loadGoogleScript();
    });

    return {
      name,
      email,
      password,
      loading,
      errorMessage,
      handleRegister,
    };
  },
};
</script>

