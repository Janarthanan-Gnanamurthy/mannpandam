<template>
  <div class="sticky top-0 z-50">
    <!-- Top Bar -->
    <div class="w-full bg-gradient-to-r from-pottery-dark via-pottery-dark to-pottery-terracotta text-white py-2.5 px-4 hidden md:flex items-center justify-between text-sm shadow-modern">
      <div class="container mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2 cursor-pointer hover:text-pottery-accent transition-smooth group">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span class="font-medium">Deliver to {{ authStore.isAuthenticated ? authStore.user?.username || 'User' : 'Guest' }}</span>
          </div>
        </div>
        <div class="flex items-center gap-6">
          <router-link v-if="!authStore.isAuthenticated" to="/login" class="hover:text-pottery-accent transition-smooth font-medium">
            Sign In
          </router-link>
          <router-link v-if="authStore.isAuthenticated" to="/orders" class="hover:text-pottery-accent transition-smooth font-medium">
            Orders
          </router-link>
        </div>
      </div>
    </div>

    <!-- Main Navbar -->
    <div class="navbar glass shadow-modern-lg border-b border-white/20 backdrop-blur-md">
      <div class="container mx-auto px-4 w-full">
        <div class="flex justify-between items-center gap-4 w-full">
        <!-- Logo -->
        <div class="flex-shrink-0">
          <router-link to="/" class="btn btn-ghost normal-case text-xl font-display font-bold hover:scale-105 transition-smooth group">
            <span class="text-3xl group-hover:rotate-12 transition-transform duration-300">🏺</span>
            <span class="hidden sm:inline font-display gradient-text text-2xl">MannPandam Studio</span>
          </router-link>
        </div>

        <!-- Search Bar -->
        <div class="flex-1 max-w-2xl">
          <form @submit.prevent="handleSearch" class="flex gap-0 shadow-modern rounded-full overflow-hidden">
            <div class="flex-1">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search handcrafted pottery..."
                class="input w-full rounded-r-none focus:outline-none focus:ring-2 focus:ring-primary/50 border-0 bg-white/80 backdrop-blur-sm placeholder:text-gray-400 h-12 pl-6"
              />
            </div>
            <button type="submit" class="btn btn-primary rounded-l-none px-8 h-12 hover:scale-105 transition-smooth shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </form>
        </div>

        <!-- Right Side Actions -->
        <div class="flex items-center gap-3">
          <!-- Cart -->
          <div class="dropdown dropdown-end">
            <label tabindex="0" class="btn btn-ghost btn-circle relative hover:scale-110 transition-smooth">
              <div class="indicator">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span v-if="cartStore.totalItems > 0" class="badge badge-sm badge-primary indicator-item border-2 border-white shadow-lg animate-scale-in">{{ cartStore.totalItems }}</span>
              </div>
            </label>
            <div tabindex="0" class="mt-3 z-[1] card card-compact dropdown-content w-80 glass shadow-modern-xl border border-white/30 rounded-2xl animate-fade-in">
              <div class="card-body">
                <div class="flex items-center justify-between mb-2">
                  <span class="font-display font-bold text-lg text-pottery-dark">Cart ({{ cartStore.totalItems }} items)</span>
                  <router-link to="/cart" class="text-primary text-sm hover:underline font-medium">View all</router-link>
                </div>
                <div class="divider my-2 bg-pottery-terracotta/20"></div>
                <div v-if="cartStore.items.length === 0" class="text-center py-4">
                  <p class="text-gray-500">Your cart is empty</p>
                </div>
                <div v-else class="max-h-64 overflow-y-auto space-y-2">
                  <div v-for="item in cartStore.items.slice(0, 3)" :key="item.id" class="flex gap-3 p-2 hover:bg-base-200 rounded-lg border border-pottery-terracotta/10">
                    <img :src="item.product.image_url || 'https://via.placeholder.com/60'" :alt="item.product.name" class="w-16 h-16 object-cover rounded-lg" />
                    <div class="flex-1 min-w-0">
                      <p class="font-semibold text-sm truncate text-pottery-dark">{{ item.product.name }}</p>
                      <p class="text-xs text-gray-500">Qty: {{ item.quantity }}</p>
                      <p class="text-sm font-bold text-primary">₹{{ (item.product.price * item.quantity).toFixed(2) }}</p>
                    </div>
                  </div>
                </div>
                <div v-if="cartStore.items.length > 0" class="divider my-2 bg-pottery-terracotta/20"></div>
                <div v-if="cartStore.items.length > 0" class="flex justify-between items-center mb-2">
                  <span class="font-display font-bold text-pottery-dark">Subtotal:</span>
                  <span class="text-xl font-display font-bold text-primary">₹{{ cartStore.totalPrice.toFixed(2) }}</span>
                </div>
                <div class="card-actions">
                  <router-link to="/cart" class="btn btn-primary btn-block">Go to Cart</router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Account Menu -->
          <div class="dropdown dropdown-end">
            <label tabindex="0" class="btn btn-ghost hover:scale-105 transition-smooth">
              <div class="flex flex-col items-start">
                <span class="text-xs text-gray-500 hidden sm:inline font-medium">{{ authStore.isAuthenticated ? 'Hello, ' + (authStore.user?.username || 'User') : 'Hello, Sign in' }}</span>
                <span class="font-bold text-sm">Account & Lists</span>
              </div>
            </label>
            <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-3 glass shadow-modern-xl rounded-2xl w-56 border border-white/30 animate-fade-in">
              <li v-if="authStore.isAuthenticated">
                <a class="justify-between">
                  <span class="text-pottery-dark">Account</span>
                  <span class="badge badge-primary badge-sm">{{ authStore.user?.username }}</span>
                </a>
              </li>
              <li v-if="authStore.isAuthenticated">
                <router-link to="/orders" class="text-pottery-dark">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                  My Orders
                </router-link>
              </li>
              <li v-if="authStore.isAuthenticated"><div class="divider my-1 bg-pottery-terracotta/20"></div></li>
              <li v-if="authStore.isAuthenticated">
                <a @click="handleLogout" class="text-error">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Sign Out
                </a>
              </li>
              <li v-if="!authStore.isAuthenticated">
                <router-link to="/login" class="btn btn-primary btn-sm">Sign In</router-link>
              </li>
              <li v-if="!authStore.isAuthenticated">
                <router-link to="/register" class="text-sm text-pottery-dark">New customer? Start here</router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const cartStore = useCartStore()
const router = useRouter()
const searchQuery = ref('')

if (authStore.isAuthenticated) {
  cartStore.fetchCart()
}

function handleLogout() {
  authStore.logout()
  cartStore.clearCart()
  router.push('/')
}

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/products', query: { search: searchQuery.value } })
  }
}
</script>
