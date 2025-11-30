<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold mb-2">My Orders</h1>
      <p class="text-gray-600">View and track your order history</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <!-- Empty State -->
    <div v-else-if="orders.length === 0" class="text-center py-20">
      <div class="text-6xl mb-4">📦</div>
      <p class="text-xl font-semibold mb-2">You have no orders yet</p>
      <p class="text-gray-600 mb-6">Start shopping to see your orders here</p>
      <router-link to="/products" class="btn btn-primary btn-lg">
        Start Shopping
      </router-link>
    </div>

    <!-- Orders List -->
    <div v-else class="space-y-6">
      <div
        v-for="order in orders"
        :key="order.id"
        class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl hover:shadow-modern-xl hover:scale-[1.01] transition-smooth"
      >
        <div class="card-body">
          <!-- Order Header -->
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
            <div>
              <div class="flex items-center gap-3 mb-2">
                <h2 class="text-2xl font-bold">Order #{{ order.id }}</h2>
                <div class="badge badge-lg" :class="getStatusBadgeClass(order.status)">
                  {{ order.status }}
                </div>
              </div>
              <p class="text-sm text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Placed on {{ formatDate(order.created_at) }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-3xl font-bold text-primary">₹{{ order.total_amount.toFixed(2) }}</p>
              <p class="text-sm text-gray-600">{{ order.order_items.length }} item{{ order.order_items.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>

          <div class="divider"></div>

          <!-- Order Items -->
          <div class="space-y-4">
            <h3 class="font-bold text-lg">Items:</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="item in order.order_items"
                :key="item.id"
                class="flex gap-4 p-4 bg-base-200 rounded-lg"
              >
                <img
                  :src="item.product?.image_url || 'https://via.placeholder.com/80'"
                  :alt="item.product?.name || 'Product'"
                  class="w-20 h-20 object-cover rounded"
                />
                <div class="flex-1">
                  <p class="font-semibold">{{ item.product?.name || 'Product' }}</p>
                  <p class="text-sm text-gray-600">Quantity: {{ item.quantity }}</p>
                  <p class="text-lg font-bold text-primary mt-1">
                    ₹{{ (item.price * item.quantity).toFixed(2) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="divider"></div>

          <!-- Shipping Address -->
          <div class="bg-base-200 p-4 rounded-lg">
            <div class="flex items-start gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <div>
                <p class="font-semibold mb-1">Shipping Address:</p>
                <p class="text-gray-700">{{ order.shipping_address }}</p>
              </div>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="card-actions justify-end mt-4">
            <button class="btn btn-outline btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              View Invoice
            </button>
            <router-link :to="`/track/${order.id}`" class="btn btn-primary">
              Track Package
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const orders = ref([])
const loading = ref(true)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  await fetchOrders()
})

async function fetchOrders() {
  try {
    const response = await api.get('/orders/')
    orders.value = response.data
  } catch (error) {
    console.error('Error fetching orders:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getStatusBadgeClass(status) {
  const statusLower = status?.toLowerCase() || ''
  if (statusLower.includes('pending')) return 'badge-warning'
  if (statusLower.includes('completed') || statusLower.includes('delivered')) return 'badge-success'
  if (statusLower.includes('cancelled')) return 'badge-error'
  if (statusLower.includes('processing') || statusLower.includes('shipped')) return 'badge-info'
  return 'badge-primary'
}
</script>
