<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-base-200 via-base-100 to-base-200 py-12 px-4">
    <div class="card w-full max-w-md glass shadow-modern-xl border border-white/30 rounded-2xl backdrop-blur-md animate-fade-in">
      <div class="card-body">
        <div class="text-center mb-6">
          <router-link to="/" class="inline-block mb-4">
            <span class="text-4xl font-display font-bold text-primary">🏺 MannPandam Studio</span>
          </router-link>
          <h2 class="text-3xl font-display font-bold text-pottery-dark">Sign In</h2>
          <p class="text-gray-600 mt-2">Welcome back! Please sign in to your account</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Username</span>
            </label>
            <input
              v-model="username"
              type="text"
              placeholder="Enter your username"
              class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm border-gray-200 rounded-xl h-12"
              required
              autocomplete="username"
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Password</span>
            </label>
            <input
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm border-gray-200 rounded-xl h-12"
              required
              autocomplete="current-password"
            />
            <label class="label">
              <a href="#" class="label-text-alt link link-primary">Forgot password?</a>
            </label>
          </div>

          <div v-if="error" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <div class="form-control mt-6">
            <button type="submit" class="btn btn-primary btn-lg w-full rounded-full hover:scale-105 transition-smooth shadow-modern-lg" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner"></span>
              <span v-else>Sign In</span>
            </button>
          </div>
        </form>

        <div class="divider bg-pottery-terracotta/20">OR</div>

        <div class="text-center">
          <p class="text-gray-600">
            Don't have an account?
            <router-link to="/register" class="link link-primary font-semibold">Create one here</router-link>
          </p>
        </div>

        <!-- Additional Info -->
        <div class="mt-6 p-4 glass rounded-xl border border-white/30 backdrop-blur-sm">
          <p class="text-xs text-gray-600 text-center">
            By continuing, you agree to MannPandam Studio's Conditions of Use and Privacy Notice.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    await cartStore.fetchCart()
    router.push('/')
  } catch (err) {
    error.value = 'Invalid username or password. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
