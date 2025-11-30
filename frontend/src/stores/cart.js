import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)

  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => sum + (item.product.price * item.quantity), 0)
  })

  async function fetchCart() {
    loading.value = true
    try {
      const response = await api.get('/cart/')
      items.value = response.data
    } catch (error) {
      console.error('Error fetching cart:', error)
    } finally {
      loading.value = false
    }
  }

  async function addToCart(productId, quantity = 1) {
    try {
      await api.post('/cart/', { product_id: productId, quantity })
      await fetchCart()
    } catch (error) {
      console.error('Error adding to cart:', error)
      throw error
    }
  }

  async function updateQuantity(itemId, quantity) {
    try {
      await api.put(`/cart/${itemId}?quantity=${quantity}`)
      await fetchCart()
    } catch (error) {
      console.error('Error updating cart:', error)
      throw error
    }
  }

  async function removeFromCart(itemId) {
    try {
      await api.delete(`/cart/${itemId}`)
      await fetchCart()
    } catch (error) {
      console.error('Error removing from cart:', error)
      throw error
    }
  }

  async function clearCart() {
    try {
      await api.delete('/cart/')
      items.value = []
    } catch (error) {
      console.error('Error clearing cart:', error)
      throw error
    }
  }

  return {
    items,
    loading,
    totalItems,
    totalPrice,
    fetchCart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart
  }
})

