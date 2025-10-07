<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <router-link to="/" class="text-3xl font-extrabold text-indigo-600 tracking-tight">
          Souraksh
        </router-link>
        <h2 class="mt-4 text-2xl font-bold text-gray-900">
          Welcome Back
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Sign in to continue to your dashboard.
        </p>
      </div>

      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input
              id="email-address"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="email"
              placeholder="Email address"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              v-model="password"
              placeholder="Password"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
            />
          </div>

          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center">
              <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
              <label for="remember-me" class="ml-2 block text-gray-900">Remember me</label>
            </div>
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">Forgot password?</a>
          </div>

          <div>
            <button
              type="submit"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-transform transform hover:scale-[1.02]"
            >
              Sign In
            </button>
          </div>
        </form>

        <div class="my-6 flex items-center">
          <div class="flex-grow border-t border-gray-200"></div>
          <span class="mx-4 text-xs font-medium text-gray-500 uppercase">Or</span>
          <div class="flex-grow border-t border-gray-200"></div>
        </div>

        <div id="google-signin-button-container-login" class="flex justify-center"></div>
        <div v-if="errorMessage" class="mt-4 text-red-600 text-sm text-center">
          {{ errorMessage }}
        </div>
      </div>

      <p class="text-center text-sm text-gray-600">
        Don't have an account?
        <router-link to="/register" class="font-medium text-indigo-600 hover:text-indigo-500">
          Sign up
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
  name: 'Login',
  setup() {
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const errorMessage = ref('');

    const handleLogin = async () => {
      try {
        const userData = { email: email.value, password: password.value };
        const response = await authService.login(userData);
        globalState.isLoggedIn = true;
        globalState.user = response;
        router.push('/forecast-dashboard');
      } catch (error) {
        errorMessage.value = error.message || 'Login failed. Please check your credentials.';
        console.error('Login failed:', error.message);
      }
    };

    const handleGoogleLogin = async (googleResponse) => {
        try {
            const response = await authService.loginWithGoogle(googleResponse.credential);
            globalState.isLoggedIn = true;
            globalState.user = response;
            router.push('/forecast-dashboard');
        } catch(error) {
            errorMessage.value = error.message || 'Google Sign-In failed. Please try again.';
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
                    document.getElementById('google-signin-button-container-login'),
                    { theme: 'outline', size: 'large', width: '300' }
                );
            } else {
                console.error("Google object not found after script load.");
                errorMessage.value = "Could not initialize Google Sign-In. Please try again.";
            }
        } catch(error) {
             console.error("Error initializing Google Sign-In:", error);
             errorMessage.value = "An error occurred with Google Sign-In.";
        }
    };

    onMounted(() => {
        loadGoogleScript();
    });

    return {
      email,
      password,
      errorMessage,
      handleLogin,
    };
  },
};
</script>

