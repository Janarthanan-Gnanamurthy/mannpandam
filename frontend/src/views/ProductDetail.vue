<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <!-- Product Not Found -->
    <div v-else-if="!product" class="text-center py-20">
      <div class="text-6xl mb-4">😕</div>
      <p class="text-xl font-semibold mb-2">Product not found</p>
      <router-link to="/products" class="btn btn-primary">Browse Products</router-link>
    </div>

    <!-- Product Details -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
      <!-- Image Section -->
      <div class="sticky top-24 self-start animate-fade-in">
        <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl overflow-hidden">
          <figure class="bg-gradient-to-br from-base-200 to-base-300 p-8">
            <img
              :src="product.image_url || 'https://via.placeholder.com/600'"
              :alt="product.name"
              class="w-full h-auto max-h-[600px] object-contain rounded-xl"
            />
          </figure>
        </div>
      </div>

      <!-- Info Section -->
      <div class="animate-slide-up">
        <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
          <div class="card-body">
            <h1 class="text-3xl md:text-4xl font-display font-bold mb-4 text-pottery-dark">{{ product.name }}</h1>
            
            <!-- Rating -->
            <div class="flex items-center gap-3 mb-4">
              <div class="rating rating-md">
                <input
                  v-for="i in 5"
                  :key="i"
                  type="radio"
                  :class="`mask mask-star-2 ${i <= Math.round(product.rating || 0) ? 'bg-pottery-accent' : 'bg-gray-300'}`"
                  disabled
                />
              </div>
              <span class="text-lg font-semibold">{{ product.rating?.toFixed(1) || '0.0' }}</span>
              <span class="text-gray-500">({{ product.review_count || 0 }} reviews)</span>
            </div>

            <div class="divider bg-pottery-terracotta/20"></div>

            <!-- Price -->
            <div class="mb-6">
              <p class="text-4xl font-display font-bold text-primary mb-2">₹{{ product.price.toFixed(2) }}</p>
              <p v-if="product.stock > 0" class="text-success font-semibold flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                In Stock ({{ product.stock }} available)
              </p>
              <p v-else class="text-error font-semibold">Out of Stock</p>
            </div>

            <!-- Description -->
            <div class="mb-6">
              <h3 class="text-xl font-display font-bold mb-2 text-pottery-dark">About this piece</h3>
              <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ product.description }}</p>
            </div>

            <div class="divider bg-pottery-terracotta/20"></div>

            <!-- Quantity Selector -->
            <div class="mb-6">
              <label class="label">
                <span class="label-text font-semibold">Quantity:</span>
              </label>
              <div class="flex items-center gap-4">
                <button
                  @click="decreaseQuantity"
                  class="btn btn-circle btn-outline"
                  :disabled="quantity <= 1"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                </button>
                <span class="text-2xl font-semibold w-12 text-center">{{ quantity }}</span>
                <button
                  @click="increaseQuantity"
                  class="btn btn-circle btn-outline"
                  :disabled="quantity >= product.stock"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span class="text-sm text-gray-500">(Max: {{ product.stock }})</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-4">
              <button
                @click="addToCart"
                class="btn btn-primary btn-lg flex-1 rounded-full hover:scale-105 transition-smooth shadow-modern-lg"
                :disabled="addingToCart || product.stock === 0"
              >
                <span v-if="addingToCart" class="loading loading-spinner"></span>
                <span v-else class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  Add to Cart
                </span>
              </button>
              <button
                class="btn btn-outline btn-primary btn-lg rounded-full hover:scale-105 transition-smooth border-2"
                :disabled="product.stock === 0"
                @click="buyNow"
              >
                Buy Now
              </button>
            </div>

            <!-- Additional Info -->
            <div class="mt-6 space-y-2 text-sm glass p-5 rounded-2xl border border-white/30 backdrop-blur-sm">
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Handcrafted by skilled artisans</span>
              </div>
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Free shipping on orders over ₹50</span>
              </div>
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>30-day return policy</span>
              </div>
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Secure payment</span>
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
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const product = ref(null)
const loading = ref(true)
const quantity = ref(1)
const addingToCart = ref(false)
const cartStore = useCartStore()
const authStore = useAuthStore()

onMounted(async () => {
  await fetchProduct()
})

async function fetchProduct() {
  try {
    const response = await api.get(`/products/${route.params.id}`)
    product.value = response.data
    // Reset quantity if it exceeds stock
    if (quantity.value > product.value.stock) {
      quantity.value = Math.max(1, product.value.stock)
    }
  } catch (error) {
    console.error('Error fetching product:', error)
  } finally {
    loading.value = false
  }
}

function increaseQuantity() {
  if (quantity.value < product.value.stock) {
    quantity.value++
  }
}

function decreaseQuantity() {
  if (quantity.value > 1) {
    quantity.value--
  }
}

async function addToCart() {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  addingToCart.value = true
  try {
    await cartStore.addToCart(product.value.id, quantity.value)
    // Show success toast (you can replace with a proper toast component)
    alert('Product added to cart!')
  } catch (error) {
    console.error('Error adding to cart:', error)
    alert('Failed to add product to cart')
  } finally {
    addingToCart.value = false
  }
}

async function buyNow() {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  try {
    await cartStore.addToCart(product.value.id, quantity.value)
    router.push('/checkout')
  } catch (error) {
    console.error('Error adding to cart:', error)
    alert('Failed to add product to cart')
  }
}
</script>
