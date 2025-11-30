<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold mb-2">Track Your Package</h1>
      <p class="text-gray-600">Monitor your order status in real-time</p>
    </div>

    <!-- Order Selection / Search -->
    <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl mb-8">
      <div class="card-body">
        <div class="flex flex-col md:flex-row gap-4 items-end">
          <div class="flex-1">
            <label class="label">
              <span class="label-text font-semibold">Enter Order ID</span>
            </label>
            <input
              v-model="orderIdInput"
              type="text"
              placeholder="Enter order ID"
              class="input input-bordered w-full"
              @keyup.enter="fetchOrder"
            />
          </div>
          <button @click="fetchOrder" class="btn btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Track Package
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
      <div class="card-body text-center py-20">
        <div class="text-6xl mb-4">📦</div>
        <p class="text-xl font-semibold mb-2 text-error">{{ error }}</p>
        <p class="text-gray-600 mb-6">Please check your order ID and try again</p>
        <button @click="fetchOrder" class="btn btn-primary">Try Again</button>
      </div>
    </div>

    <!-- Tracking Display -->
    <div v-else-if="order" class="space-y-6">
      <!-- Order Info Card -->
      <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
        <div class="card-body">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h2 class="text-2xl font-bold mb-2">Order #{{ order.id }}</h2>
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
        </div>
      </div>

      <!-- Tracking Timeline -->
      <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
        <div class="card-body">
          <h3 class="text-2xl font-bold mb-6">Package Status</h3>
          
          <!-- Timeline -->
          <div class="relative">
            <!-- Timeline Line -->
            <div class="absolute left-8 top-0 bottom-0 w-1 bg-gray-200" :style="{ height: '100%' }"></div>
            <div 
              class="absolute left-8 top-0 w-1 bg-primary transition-all duration-500"
              :style="{ height: getProgressHeight() + '%' }"
            ></div>

            <!-- Timeline Steps -->
            <div class="space-y-8">
              <!-- Pending Stage -->
              <div class="relative flex items-start gap-6">
                <div class="relative z-10">
                  <div 
                    class="w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all duration-300"
                    :class="getStageClass('pending')"
                  >
                    <svg v-if="currentStageIndex >= 0" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span v-else>📋</span>
                  </div>
                </div>
                <div class="flex-1 pt-2">
                  <h4 class="text-xl font-bold mb-1" :class="currentStageIndex >= 0 ? 'text-primary' : 'text-gray-400'">
                    Pending
                  </h4>
                  <p class="text-gray-600 mb-2">Your order has been received and is being processed</p>
                  <p v-if="currentStageIndex >= 0" class="text-sm text-success font-medium">
                    ✓ Completed on {{ formatDate(order.created_at) }}
                  </p>
                </div>
              </div>

              <!-- Shipped Stage -->
              <div class="relative flex items-start gap-6">
                <div class="relative z-10">
                  <div 
                    class="w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all duration-300"
                    :class="getStageClass('shipped')"
                  >
                    <svg v-if="currentStageIndex >= 1" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span v-else>🚚</span>
                  </div>
                </div>
                <div class="flex-1 pt-2">
                  <h4 class="text-xl font-bold mb-1" :class="currentStageIndex >= 1 ? 'text-primary' : 'text-gray-400'">
                    Shipped
                  </h4>
                  <p class="text-gray-600 mb-2">Your package has been shipped and is on its way</p>
                  <p v-if="currentStageIndex >= 1" class="text-sm text-success font-medium">
                    ✓ Shipped on {{ getStageDate('shipped') }}
                  </p>
                </div>
              </div>

              <!-- Out for Delivery Stage -->
              <div class="relative flex items-start gap-6">
                <div class="relative z-10">
                  <div 
                    class="w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all duration-300"
                    :class="getStageClass('out_for_delivery')"
                  >
                    <svg v-if="currentStageIndex >= 2" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span v-else>🚛</span>
                  </div>
                </div>
                <div class="flex-1 pt-2">
                  <h4 class="text-xl font-bold mb-1" :class="currentStageIndex >= 2 ? 'text-primary' : 'text-gray-400'">
                    Out for Delivery
                  </h4>
                  <p class="text-gray-600 mb-2">Your package is out for delivery and will arrive soon</p>
                  <p v-if="currentStageIndex >= 2" class="text-sm text-success font-medium">
                    ✓ Out for delivery on {{ getStageDate('out_for_delivery') }}
                  </p>
                </div>
              </div>

              <!-- Delivered Stage -->
              <div class="relative flex items-start gap-6">
                <div class="relative z-10">
                  <div 
                    class="w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all duration-300"
                    :class="getStageClass('delivered')"
                  >
                    <svg v-if="currentStageIndex >= 3" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span v-else>📬</span>
                  </div>
                </div>
                <div class="flex-1 pt-2">
                  <h4 class="text-xl font-bold mb-1" :class="currentStageIndex >= 3 ? 'text-primary' : 'text-gray-400'">
                    Delivered
                  </h4>
                  <p class="text-gray-600 mb-2">Your package has been successfully delivered</p>
                  <p v-if="currentStageIndex >= 3" class="text-sm text-success font-medium">
                    ✓ Delivered on {{ getStageDate('delivered') }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Shipping Address -->
      <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
        <div class="card-body">
          <div class="flex items-start gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <div class="flex-1">
              <h3 class="font-bold text-lg mb-2">Shipping Address</h3>
              <p class="text-gray-700">{{ order.shipping_address }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Items -->
      <div class="card bg-white shadow-modern-xl border border-gray-100 rounded-2xl">
        <div class="card-body">
          <h3 class="font-bold text-lg mb-4">Order Items</h3>
          <div class="space-y-4">
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const order = ref(null)
const loading = ref(false)
const error = ref(null)
const orderIdInput = ref('')

// Define tracking stages
const stages = ['pending', 'shipped', 'out_for_delivery', 'delivered']

// Get current stage index
const currentStageIndex = computed(() => {
  if (!order.value) return -1
  const status = order.value.status?.toLowerCase() || 'pending'
  
  if (status.includes('delivered')) return 3
  if (status.includes('out') && status.includes('delivery')) return 2
  if (status.includes('shipped')) return 1
  return 0
})

// Get progress height for timeline
function getProgressHeight() {
  if (currentStageIndex.value === -1) return 0
  return ((currentStageIndex.value + 1) / stages.length) * 100
}

// Get stage class
function getStageClass(stage) {
  const stageIndex = stages.indexOf(stage)
  if (currentStageIndex.value >= stageIndex) {
    return 'bg-primary text-white shadow-modern-lg scale-110'
  }
  return 'bg-gray-200 text-gray-400'
}

// Get stage date (mock dates for now, can be enhanced with actual timestamps)
function getStageDate(stage) {
  if (!order.value) return ''
  const baseDate = new Date(order.value.created_at)
  const stageIndex = stages.indexOf(stage)
  
  // Add days based on stage
  const daysToAdd = stageIndex * 2
  baseDate.setDate(baseDate.getDate() + daysToAdd)
  
  return formatDate(baseDate.toISOString())
}

// Format date
function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Fetch order
async function fetchOrder() {
  if (!orderIdInput.value.trim()) {
    error.value = 'Please enter an order ID'
    return
  }

  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await api.get(`/orders/${orderIdInput.value}`)
    order.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Order not found. Please check your order ID.'
    order.value = null
  } finally {
    loading.value = false
  }
}

// Check if order ID is in route params
onMounted(() => {
  if (route.params.orderId) {
    orderIdInput.value = route.params.orderId
    fetchOrder()
  }
})
</script>

