<template>
  <GlassPanel variant="card" class="h-full p-4 flex flex-col gap-4">
    <div class="flex items-center justify-between mb-2">
      <h2 class="text-lg font-semibold text-white">Agent Insights</h2>
      <div class="p-1.5 rounded-full bg-system-blue/20">
        <SparklesIcon class="w-5 h-5 text-system-blue animate-pulse" />
      </div>
    </div>

    <!-- Nutrition Card -->
    <div class="bg-system-gray5/50 rounded-2xl p-4 border border-white/5">
      <div class="flex items-center gap-2 mb-3">
        <div class="w-8 h-8 rounded-full bg-system-green/20 flex items-center justify-center">
          <ChartPieIcon class="w-5 h-5 text-system-green" />
        </div>
        <span class="text-sm font-medium text-white">Nutrition</span>
      </div>
      <div class="flex justify-between items-end">
        <div>
          <div class="text-2xl font-bold text-white">550</div>
          <div class="text-xs text-system-gray">kcal detected</div>
        </div>
        <div class="h-12 w-12 rounded-full border-4 border-system-green/30 border-t-system-green"></div>
      </div>
    </div>

    <!-- Tasks Card -->
    <div class="bg-system-gray5/50 rounded-2xl p-4 border border-white/5 flex-grow">
      <div class="flex items-center gap-2 mb-3">
        <div class="w-8 h-8 rounded-full bg-system-orange/20 flex items-center justify-center">
          <CheckCircleIcon class="w-5 h-5 text-system-orange" />
        </div>
        <span class="text-sm font-medium text-white">Tasks</span>
      </div>
      <ul class="space-y-2">
        <li class="flex items-start gap-3 group cursor-pointer">
          <div class="mt-0.5 w-5 h-5 rounded-full border-2 border-system-gray4 group-hover:border-system-blue transition-colors"></div>
          <span class="text-sm text-system-gray2 group-hover:text-white transition-colors">Go to the gym</span>
        </li>
        <li class="flex items-start gap-3 group cursor-pointer">
          <div class="mt-0.5 w-5 h-5 rounded-full border-2 border-system-gray4 group-hover:border-system-blue transition-colors"></div>
          <span class="text-sm text-system-gray2 group-hover:text-white transition-colors">Buy groceries</span>
        </li>
      </ul>
    </div>
  </GlassPanel>
</template>

<script setup lang="ts">
import GlassPanel from './GlassPanel.vue';
import { SparklesIcon, ChartPieIcon, CheckCircleIcon } from '@heroicons/vue/24/outline';
</script>
