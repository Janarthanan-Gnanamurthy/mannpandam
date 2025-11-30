<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-base-200 via-base-100 to-base-200 py-12 px-4">
    <div class="card w-full max-w-md glass shadow-modern-xl border border-white/30 rounded-2xl backdrop-blur-md animate-fade-in">
      <div class="card-body">
        <div class="text-center mb-6">
          <router-link to="/" class="inline-block mb-4">
            <span class="text-4xl font-display font-bold text-primary">🏺 MannPandam Studio</span>
          </router-link>
          <h2 class="text-3xl font-display font-bold text-pottery-dark">Create Account</h2>
          <p class="text-gray-600 mt-2">Join MannPandam Studio and discover handcrafted pottery today!</p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Email</span>
            </label>
            <input
              v-model="email"
              type="email"
              placeholder="Enter your email"
              class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm border-gray-200 rounded-xl h-12"
              required
              autocomplete="email"
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Username</span>
            </label>
            <input
              v-model="username"
              type="text"
              placeholder="Choose a username"
              class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm border-gray-200 rounded-xl h-12"
              required
              autocomplete="username"
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Full Name</span>
              <span class="label-text-alt text-gray-500">(Optional)</span>
            </label>
            <input
              v-model="fullName"
              type="text"
              placeholder="Enter your full name"
              class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm border-gray-200 rounded-xl h-12"
              autocomplete="name"
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Password</span>
            </label>
            <input
              v-model="password"
              type="password"
              placeholder="Create a password"
              class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm border-gray-200 rounded-xl h-12"
              required
              autocomplete="new-password"
            />
            <label class="label">
              <span class="label-text-alt text-gray-500">Must be at least 8 characters</span>
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
              <span v-else>Create Account</span>
            </button>
          </div>
        </form>

        <div class="divider bg-pottery-terracotta/20">OR</div>

        <div class="text-center">
          <p class="text-gray-600">
            Already have an account?
            <router-link to="/login" class="link link-primary font-semibold">Sign in here</router-link>
          </p>
        </div>

        <!-- Terms and Conditions -->
        <div class="mt-6 p-4 glass rounded-xl border border-white/30 backdrop-blur-sm">
          <p class="text-xs text-gray-600 text-center">
            By creating an account, you agree to MannPandam Studio's
            <a href="#" class="link link-primary">Conditions of Use</a> and
            <a href="#" class="link link-primary">Privacy Notice</a>.
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

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const username = ref('')
const fullName = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await authStore.register({
      email: email.value,
      username: username.value,
      full_name: fullName.value,
      password: password.value
    })
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
