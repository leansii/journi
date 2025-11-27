<template>
  <div 
    class="backdrop-blur-xl border border-white/10 transition-all duration-300"
    :class="[
      variant === 'sidebar' ? 'bg-system-gray6/50' : '',
      variant === 'card' ? 'bg-system-gray6/40 rounded-[20px] shadow-lg' : '',
      variant === 'modal' ? 'bg-system-gray6/80 rounded-[24px] shadow-2xl' : ''
    ]"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'sidebar' | 'card' | 'modal'
}>()
</script>
