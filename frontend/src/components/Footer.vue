<template>
  <footer class="bg-gradient-to-br from-pottery-dark via-pottery-dark to-pottery-terracotta text-white mt-auto shadow-modern-lg">
    <!-- Back to Top -->
    <div class="bg-black/20 backdrop-blur-sm py-4 text-center cursor-pointer hover:bg-black/30 transition-smooth border-b border-white/10" @click="scrollToTop">
      <span class="text-sm font-semibold flex items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
        Back to top
      </span>
    </div>

    <!-- Main Footer Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Column 1 -->
        <div>
          <h3 class="font-display font-bold text-lg mb-4 text-pottery-accent">About MannPandam Studio</h3>
          <ul class="space-y-3 text-sm">
            <li><a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Our Story</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Artisan Community</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Craftsmanship</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Sustainability</a></li>
          </ul>
        </div>

        <!-- Column 2 -->
        <div>
          <h3 class="font-display font-bold text-lg mb-4 text-pottery-accent">Collections</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Traditional Pottery</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Modern Designs</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Custom Orders</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Gift Collections</a></li>
          </ul>
        </div>

        <!-- Column 3 -->
        <div>
          <h3 class="font-display font-bold text-lg mb-4 text-pottery-accent">Customer Care</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Shipping & Delivery</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Care Instructions</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Returns & Exchanges</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">FAQ</a></li>
          </ul>
        </div>

        <!-- Column 4 -->
        <div>
          <h3 class="font-display font-bold text-lg mb-4 text-pottery-accent">Connect With Us</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Contact Us</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Workshops & Events</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Newsletter</a></li>
            <li><a href="#" class="hover:text-pottery-accent transition-colors">Social Media</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Bottom Bar -->
    <div class="border-t border-white/20 bg-black/10 backdrop-blur-sm">
      <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row items-center justify-between gap-6">
          <div class="flex items-center gap-4">
            <router-link to="/" class="text-2xl font-display font-bold hover:text-pottery-accent transition-smooth hover:scale-105 flex items-center gap-2">
              <span class="text-3xl">🏺</span>
              <span class="gradient-text">MannPandam Studio</span>
            </router-link>
          </div>
          <div class="flex flex-wrap items-center justify-center gap-6 text-sm">
            <a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Terms of Service</a>
            <a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Privacy Policy</a>
            <a href="#" class="hover:text-pottery-accent transition-smooth font-medium">Cookie Policy</a>
          </div>
          <div class="text-sm text-gray-300 font-medium">
            © {{ new Date().getFullYear() }} MannPandam Studio. Handcrafted with love in India.
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
