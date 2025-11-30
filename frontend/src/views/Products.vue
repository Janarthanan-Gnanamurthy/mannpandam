<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-display font-bold mb-2 text-pottery-dark">All Products</h1>
      <p class="text-gray-600">Discover our complete collection of handcrafted pottery</p>
    </div>

    <!-- Filters and Search -->
    <div class="glass rounded-2xl shadow-modern-lg p-6 mb-8 border border-white/30 backdrop-blur-md">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <div class="form-control">
            <div class="input-group shadow-modern rounded-full overflow-hidden">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search handcrafted pottery..."
                class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 border-0 bg-white/80 backdrop-blur-sm h-12 pl-6"
                @input="debouncedSearch"
              />
              <button class="btn btn-primary rounded-l-none h-12 px-6 hover:scale-105 transition-smooth" @click="fetchProducts">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div class="w-full md:w-64">
          <select
            v-model="selectedCategory"
            class="select select-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm h-12 rounded-full border-0 shadow-modern"
            @change="fetchProducts"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
        <div class="w-full md:w-48">
          <select
            v-model="sortBy"
            class="select select-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-sm h-12 rounded-full border-0 shadow-modern"
            @change="fetchProducts"
          >
            <option value="">Sort By</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="name_asc">Name: A to Z</option>
            <option value="name_desc">Name: Z to A</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <!-- Empty State -->
    <div v-else-if="products.length === 0" class="text-center py-20">
      <div class="text-6xl mb-4">🔍</div>
      <p class="text-xl font-semibold mb-2">No products found</p>
      <p class="text-gray-600 mb-6">Try adjusting your search or filters</p>
      <button @click="clearFilters" class="btn btn-primary">Clear Filters</button>
    </div>

    <!-- Products Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div
        v-for="product in products"
        :key="product.id"
        class="card bg-white shadow-modern hover:shadow-modern-xl transition-smooth border border-gray-100 group cursor-pointer overflow-hidden rounded-2xl animate-fade-in hover:scale-[1.02]"
        @click="$router.push(`/products/${product.id}`)"
      >
        <figure class="relative overflow-hidden bg-gradient-to-br from-base-200 to-base-300">
          <img
            :src="product.image_url || 'https://via.placeholder.com/300'"
            :alt="product.name"
            class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
          />
          <div class="absolute top-4 right-4">
            <div v-if="product.stock > 0" class="badge badge-success badge-lg shadow-modern-lg backdrop-blur-sm border-0">In Stock</div>
            <div v-else class="badge badge-error badge-lg shadow-modern-lg backdrop-blur-sm border-0">Out of Stock</div>
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </figure>
        <div class="card-body p-5">
          <h2 class="card-title line-clamp-2 min-h-[3.5rem] hover:text-primary transition-colors font-display text-pottery-dark text-lg">
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
              <p v-if="product.stock" class="text-xs text-success font-medium">{{ product.stock }} available</p>
            </div>
            <button
              class="btn btn-primary btn-sm rounded-full hover:scale-105 transition-smooth shadow-modern"
              @click.stop="$router.push(`/products/${product.id}`)"
            >
              View
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Count -->
    <div v-if="!loading && products.length > 0" class="mt-8 text-center text-gray-600">
      <p>Showing {{ products.length }} product{{ products.length !== 1 ? 's' : '' }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const products = ref([])
const categories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('')
let searchTimeout = null

onMounted(async () => {
  // Check for search query in route
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
  await Promise.all([fetchProducts(), fetchCategories()])
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = { limit: 50 }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (sortBy.value) {
      params.sort = sortBy.value
    }
    const response = await api.get('/products/', { params })
    products.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const response = await api.get('/products/categories/list')
    categories.value = response.data
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchProducts()
  }, 500)
}

function clearFilters() {
  searchQuery.value = ''
  selectedCategory.value = ''
  sortBy.value = ''
  fetchProducts()
}
</script>
