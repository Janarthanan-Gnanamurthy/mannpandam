import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  function setUser(userData) {
    user.value = userData
  }

  async function login(username, password) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData)
    setToken(response.data.access_token)
    await fetchUser()
    return response.data
  }

  async function register(userData) {
    const response = await api.post('/auth/register', userData)
    await login(userData.username, userData.password)
    return response.data
  }

  async function fetchUser() {
    try {
      const response = await api.get('/auth/me')
      setUser(response.data)
    } catch (error) {
      logout()
    }
  }

  function logout() {
    setToken(null)
    setUser(null)
  }

  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
})

