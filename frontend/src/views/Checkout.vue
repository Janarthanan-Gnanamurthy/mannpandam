<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold mb-2">Checkout</h1>
      <p class="text-gray-600">Review your order and complete your purchase</p>
    </div>

    <!-- Loading State -->
    <div v-if="cartStore.loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <!-- Empty Cart -->
    <div v-else-if="cartStore.items.length === 0" class="text-center py-20">
      <div class="text-6xl mb-4">🛒</div>
      <p class="text-xl font-semibold mb-2">Your cart is empty</p>
      <p class="text-gray-600 mb-6">Add items to your cart before checkout</p>
      <router-link to="/products" class="btn btn-primary btn-lg">Continue Shopping</router-link>
    </div>

    <!-- Checkout Form -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Shipping Information -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Shipping Address -->
        <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Shipping Address
            </h2>
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Full Address</span>
              </label>
              <textarea
                v-model="shippingAddress"
                class="textarea textarea-bordered h-32 focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter your full shipping address including street, city, state, and zip code"
                rows="4"
              ></textarea>
              <label class="label">
                <span class="label-text-alt text-gray-500">Please provide a complete address for delivery</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Payment Method (Placeholder) -->
        <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              Payment Method
            </h2>
            <div class="alert alert-info">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>Payment processing will be handled securely during order placement.</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="lg:col-span-1">
        <div class="card glass shadow-modern-xl border border-white/30 sticky top-24 rounded-2xl backdrop-blur-md">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-4">Order Summary</h2>
            <div class="divider"></div>

            <!-- Order Items -->
            <div class="space-y-3 max-h-64 overflow-y-auto">
              <div
                v-for="item in cartStore.items"
                :key="item.id"
                class="flex gap-3"
              >
                <img
                  :src="item.product.image_url || 'https://via.placeholder.com/60'"
                  :alt="item.product.name"
                  class="w-16 h-16 object-cover rounded"
                />
                <div class="flex-1 min-w-0">
                  <p class="font-semibold text-sm line-clamp-2">{{ item.product.name }}</p>
                  <p class="text-xs text-gray-500">Qty: {{ item.quantity }}</p>
                  <p class="text-sm font-bold text-primary">₹{{ (item.product.price * item.quantity).toFixed(2) }}</p>
                </div>
              </div>
            </div>

            <div class="divider"></div>

            <!-- Price Breakdown -->
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600">Subtotal ({{ cartStore.totalItems }} items):</span>
                <span class="font-semibold">₹{{ cartStore.totalPrice.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Shipping:</span>
                <span class="font-semibold text-success">FREE</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Tax:</span>
                <span class="font-semibold">₹{{ (cartStore.totalPrice * 0.1).toFixed(2) }}</span>
              </div>
            </div>

            <div class="divider"></div>

            <!-- Total -->
            <div class="flex justify-between items-center">
              <span class="text-xl font-bold">Total:</span>
              <span class="text-2xl font-bold text-primary">₹{{ (cartStore.totalPrice * 1.1).toFixed(2) }}</span>
            </div>

            <!-- Place Order Button -->
            <div class="card-actions mt-6">
              <button
                @click="placeOrder"
                class="btn btn-primary btn-block btn-lg rounded-full hover:scale-105 transition-smooth shadow-modern-lg"
                :disabled="!shippingAddress.trim() || placingOrder"
              >
                <span v-if="placingOrder" class="loading loading-spinner"></span>
                <span v-else class="flex items-center gap-2">
                  Place Order
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </button>
            </div>

            <!-- Security Badge -->
            <div class="mt-4 text-center">
              <div class="flex items-center justify-center gap-2 text-sm text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span>Secure Checkout</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const shippingAddress = ref('')
const placingOrder = ref(false)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  await cartStore.fetchCart()
})

async function placeOrder() {
  if (!shippingAddress.value.trim()) {
    alert('Please enter a shipping address')
    return
  }

  placingOrder.value = true
  try {
    await api.post('/orders/', { shipping_address: shippingAddress.value })
    await cartStore.clearCart()
    router.push('/orders')
  } catch (error) {
    console.error('Error placing order:', error)
    alert('Failed to place order. Please try again.')
  } finally {
    placingOrder.value = false
  }
}
</script>
