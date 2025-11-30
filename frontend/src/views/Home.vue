<template>
  <div>
    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-br from-pottery-terracotta via-primary to-pottery-ochre text-white overflow-hidden">
      <div class="absolute inset-0 bg-black/10"></div>
      <div class="container mx-auto px-4 py-20 md:py-32 relative z-10">
        <div class="max-w-3xl animate-slide-up">
          <h1 class="text-5xl md:text-7xl font-display font-bold mb-6 leading-tight drop-shadow-lg">
            Handcrafted Indian Pottery
          </h1>
          <p class="text-xl md:text-2xl mb-10 opacity-95 font-light leading-relaxed">
            Discover timeless elegance in every piece. Handcrafted with love, tradition, and modern artistry.
          </p>
          <div class="flex flex-col sm:flex-row gap-4">
            <router-link to="/products" class="btn btn-lg bg-white text-pottery-dark hover:bg-pottery-cream border-none shadow-modern-xl font-semibold hover:scale-105 transition-smooth px-8 rounded-full">
              Explore Collection
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
            <router-link to="/products" class="btn btn-lg btn-outline border-2 border-white/80 text-white hover:bg-white/20 hover:border-white backdrop-blur-sm font-semibold px-8 rounded-full transition-smooth">
              Browse All
            </router-link>
          </div>
        </div>
      </div>
      <!-- Modern decorative elements -->
      <div class="absolute top-0 right-0 w-96 h-96 bg-pottery-accent opacity-20 rounded-full -mr-48 -mt-48 blur-3xl animate-pulse"></div>
      <div class="absolute bottom-0 left-0 w-72 h-72 bg-white opacity-15 rounded-full -ml-36 -mb-36 blur-3xl"></div>
      <div class="absolute top-1/2 right-1/4 w-64 h-64 bg-pottery-ochre opacity-10 rounded-full blur-3xl"></div>
    </div>

    <!-- Featured Products Section -->
    <div class="container mx-auto px-4 py-12">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-3xl md:text-4xl font-display font-bold text-pottery-dark">Featured Handcrafted Pieces</h2>
        <router-link to="/products" class="btn btn-ghost text-primary hover:text-primary-focus font-medium">
          View All
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </router-link>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <span class="loading loading-spinner loading-lg text-primary"></span>
      </div>

      <div v-else-if="featuredProducts.length === 0" class="text-center py-20">
        <p class="text-xl text-gray-500">No products available at the moment</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="product in featuredProducts"
          :key="product.id"
          class="card bg-white shadow-modern hover:shadow-modern-xl transition-smooth border border-gray-100 group overflow-hidden rounded-2xl animate-fade-in"
        >
          <figure class="relative overflow-hidden bg-gradient-to-br from-base-200 to-base-300">
            <img
              :src="product.image_url || 'https://via.placeholder.com/300'"
              :alt="product.name"
              class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
            />
            <div class="absolute top-4 right-4">
              <div class="badge badge-primary badge-lg shadow-modern-lg backdrop-blur-sm bg-primary/90 border-0">Handcrafted</div>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </figure>
          <div class="card-body p-5">
            <h2 class="card-title line-clamp-2 min-h-[3.5rem] font-display text-pottery-dark text-lg group-hover:text-primary transition-colors">
              {{ product.name }}
            </h2>
            <p class="text-gray-600 text-sm line-clamp-2 min-h-[2.5rem] leading-relaxed">
              {{ product.description?.substring(0, 100) }}...
            </p>
            
            <!-- Rating -->
            <div class="flex items-center gap-2 mt-2">
              <div class="rating rating-sm">
                <input
                  v-for="i in 5"
                  :key="i"
                  type="radio"
                  :class="`mask mask-star-2 ${i <= Math.round(product.rating || 0) ? 'bg-pottery-accent' : 'bg-gray-300'}`"
                  disabled
                />
              </div>
              <span class="text-xs text-gray-500">({{ product.review_count || 0 }})</span>
            </div>

            <div class="card-actions justify-between items-center mt-4 pt-4 border-t border-gray-100">
              <div>
                <p class="text-2xl font-display font-bold text-primary">₹{{ product.price.toFixed(2) }}</p>
                <p v-if="product.stock" class="text-xs text-success font-medium">In Stock</p>
              </div>
              <router-link
                :to="`/products/${product.id}`"
                class="btn btn-primary btn-sm rounded-full hover:scale-105 transition-smooth shadow-modern"
              >
                View Details
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Sections -->
    <div class="bg-gradient-to-b from-white via-base-200 to-base-200 py-16">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center p-8 bg-white rounded-2xl shadow-modern hover:shadow-modern-xl transition-smooth border border-gray-100 group hover:scale-105">
            <div class="text-6xl mb-5 group-hover:scale-110 transition-transform duration-300">🏺</div>
            <h3 class="font-display font-bold text-xl mb-3 text-pottery-dark">Handcrafted Quality</h3>
            <p class="text-gray-600 leading-relaxed">Each piece is uniquely made by skilled artisans</p>
          </div>
          <div class="text-center p-8 bg-white rounded-2xl shadow-modern hover:shadow-modern-xl transition-smooth border border-gray-100 group hover:scale-105">
            <div class="text-6xl mb-5 group-hover:scale-110 transition-transform duration-300">🌿</div>
            <h3 class="font-display font-bold text-xl mb-3 text-pottery-dark">Eco-Friendly</h3>
            <p class="text-gray-600 leading-relaxed">Made with natural materials and traditional methods</p>
          </div>
          <div class="text-center p-8 bg-white rounded-2xl shadow-modern hover:shadow-modern-xl transition-smooth border border-gray-100 group hover:scale-105">
            <div class="text-6xl mb-5 group-hover:scale-110 transition-transform duration-300">✨</div>
            <h3 class="font-display font-bold text-xl mb-3 text-pottery-dark">Timeless Design</h3>
            <p class="text-gray-600 leading-relaxed">Blending traditional Indian artistry with modern aesthetics</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const featuredProducts = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.get('/products/?limit=8')
    featuredProducts.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
  } finally {
    loading.value = false
  }
})
</script>
