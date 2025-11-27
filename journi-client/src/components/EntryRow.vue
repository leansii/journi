<template>
  <div 
    class="group flex items-center p-3 mb-1 rounded-xl cursor-pointer transition-all duration-200"
    :class="active ? 'bg-white/10 shadow-sm' : 'hover:bg-white/5'"
  >
    <div 
      class="p-2 rounded-lg mr-3 transition-colors"
      :class="active ? 'bg-system-blue text-white' : 'bg-system-gray5 text-system-gray'"
    >
      <component :is="icon" class="w-5 h-5" />
    </div>
    <div class="flex-grow min-w-0">
      <h3 class="text-sm font-medium text-white truncate">{{ title }}</h3>
      <p class="text-xs text-system-gray truncate">{{ subtitle }}</p>
    </div>
    <div v-if="status" class="w-2 h-2 rounded-full" :class="statusColor"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  title: string
  subtitle: string
  active?: boolean
  icon: any
  status?: 'pending' | 'processed' | 'error'
}>()

const statusColor = computed(() => {
  switch (props.status) {
    case 'pending': return 'bg-system-orange animate-pulse'
    case 'processed': return 'bg-system-green'
    case 'error': return 'bg-system-red'
    default: return ''
  }
})
</script>
