<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold mb-2">Shopping Cart</h1>
      <p v-if="cartStore.items.length > 0" class="text-gray-600">
        {{ cartStore.items.length }} item{{ cartStore.items.length !== 1 ? 's' : '' }} in your cart
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="cartStore.loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <!-- Empty Cart -->
    <div v-else-if="cartStore.items.length === 0" class="text-center py-20">
      <div class="text-6xl mb-4">🛒</div>
      <p class="text-xl font-semibold mb-2">Your cart is empty</p>
      <p class="text-gray-600 mb-6">Start shopping to add items to your cart</p>
      <router-link to="/products" class="btn btn-primary btn-lg">
        Continue Shopping
      </router-link>
    </div>

    <!-- Cart Content -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Cart Items -->
      <div class="lg:col-span-2 space-y-4">
        <div
          v-for="item in cartStore.items"
          :key="item.id"
          class="card bg-white shadow-modern border border-gray-100 rounded-2xl hover:shadow-modern-lg transition-smooth"
        >
          <div class="card-body">
            <div class="flex flex-col md:flex-row gap-4">
              <!-- Product Image -->
              <div class="flex-shrink-0">
                <router-link :to="`/products/${item.product.id}`">
                  <img
                    :src="item.product.image_url || 'https://via.placeholder.com/150'"
                    :alt="item.product.name"
                    class="w-32 h-32 object-cover rounded-lg hover:opacity-80 transition-opacity"
                  />
                </router-link>
              </div>

              <!-- Product Info -->
              <div class="flex-1 min-w-0">
                <router-link :to="`/products/${item.product.id}`" class="hover:text-primary transition-colors">
                  <h2 class="text-xl font-bold mb-2 line-clamp-2">{{ item.product.name }}</h2>
                </router-link>
                <p class="text-gray-600 text-sm line-clamp-2 mb-2">
                  {{ item.product.description?.substring(0, 100) }}...
                </p>
                <p class="text-lg font-bold text-primary">₹{{ item.product.price.toFixed(2) }}</p>
              </div>

              <!-- Quantity and Actions -->
              <div class="flex flex-col items-end gap-4">
                <!-- Quantity Controls -->
                <div class="flex items-center gap-3">
                  <label class="text-sm text-gray-600">Qty:</label>
                  <div class="flex items-center gap-2">
                    <button
                      @click="updateQuantity(item.id, item.quantity - 1)"
                      class="btn btn-circle btn-sm btn-outline"
                      :disabled="updating === item.id"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                      </svg>
                    </button>
                    <span class="text-lg font-semibold w-8 text-center">{{ item.quantity }}</span>
                    <button
                      @click="updateQuantity(item.id, item.quantity + 1)"
                      class="btn btn-circle btn-sm btn-outline"
                      :disabled="updating === item.id"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Subtotal -->
                <div class="text-right">
                  <p class="text-sm text-gray-600">Subtotal:</p>
                  <p class="text-xl font-bold text-primary">₹{{ (item.product.price * item.quantity).toFixed(2) }}</p>
                </div>

                <!-- Remove Button -->
                <button
                  @click="removeItem(item.id)"
                  class="btn btn-error btn-sm"
                  :disabled="removing === item.id"
                >
                  <span v-if="removing === item.id" class="loading loading-spinner loading-sm"></span>
                  <span v-else class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Remove
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Continue Shopping -->
        <div class="card bg-base-100 shadow-lg border border-base-300">
          <div class="card-body">
            <router-link to="/products" class="btn btn-ghost w-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Continue Shopping
            </router-link>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="lg:col-span-1">
        <div class="card glass shadow-modern-xl border border-white/30 sticky top-24 rounded-2xl backdrop-blur-md">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-4">Order Summary</h2>
            <div class="divider"></div>
            
            <div class="space-y-3">
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

            <div class="flex justify-between items-center">
              <span class="text-xl font-bold">Total:</span>
              <span class="text-2xl font-bold text-primary">₹{{ (cartStore.totalPrice * 1.1).toFixed(2) }}</span>
            </div>

            <div class="card-actions mt-6">
              <router-link to="/checkout" class="btn btn-primary btn-block btn-lg rounded-full hover:scale-105 transition-smooth shadow-modern-lg">
                Proceed to Checkout
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </router-link>
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
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()
const updating = ref(null)
const removing = ref(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  await cartStore.fetchCart()
})

async function updateQuantity(itemId, newQuantity) {
  if (newQuantity < 1) {
    await removeItem(itemId)
    return
  }
  updating.value = itemId
  try {
    await cartStore.updateQuantity(itemId, newQuantity)
  } catch (error) {
    console.error('Error updating quantity:', error)
    alert('Failed to update quantity')
  } finally {
    updating.value = null
  }
}

async function removeItem(itemId) {
  if (!confirm('Are you sure you want to remove this item from your cart?')) {
    return
  }
  removing.value = itemId
  try {
    await cartStore.removeFromCart(itemId)
  } catch (error) {
    console.error('Error removing item:', error)
    alert('Failed to remove item')
  } finally {
    removing.value = null
  }
}
</script>
