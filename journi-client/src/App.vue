<template>
  <div class="h-screen w-full bg-system-background text-white flex overflow-hidden font-sans antialiased selection:bg-system-blue/30">
    <!-- Background Gradient Mesh (Subtle) -->
    <div class="fixed inset-0 z-0 pointer-events-none">
      <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-system-blue/10 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-system-purple/10 rounded-full blur-[120px]"></div>
    </div>

    <!-- Left Sidebar -->
    <GlassPanel variant="sidebar" class="w-80 flex-shrink-0 z-10 flex flex-col border-r border-white/5">
      <div class="p-4 pt-6">
        <h1 class="text-2xl font-bold tracking-tight mb-6 flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-system-blue to-purple-500 flex items-center justify-center">
            <span class="text-lg">J</span>
          </div>
          Journi
        </h1>
        
        <button class="w-full py-2 px-4 bg-white/10 hover:bg-white/20 rounded-xl text-sm font-medium transition-colors flex items-center justify-center gap-2 mb-6">
          <PlusIcon class="w-4 h-4" />
          New Entry
        </button>

        <div class="space-y-1">
          <h2 class="text-xs font-semibold text-system-gray uppercase tracking-wider mb-2 px-2">Today</h2>
          <EntryRow 
            title="Lunch at Sweetgreen" 
            subtitle="12:30 PM" 
            :icon="ClockIcon" 
            :active="true"
            status="processed"
          />
          <EntryRow 
            title="Morning Standup" 
            subtitle="09:00 AM" 
            :icon="CalendarIcon" 
            status="processed"
          />
        </div>
      </div>
    </GlassPanel>

    <!-- Main Content (Editor) -->
    <main class="flex-grow z-0 relative flex flex-col">
      <header class="h-16 flex items-center justify-between px-8 border-b border-white/5">
        <div class="text-sm text-system-gray">
          November 28, 2025
        </div>
        <div class="flex items-center gap-4">
          <span class="text-xs text-system-gray2">Saved</span>
          <button class="p-2 hover:bg-white/5 rounded-full transition-colors">
            <EllipsisHorizontalIcon class="w-5 h-5 text-system-gray" />
          </button>
        </div>
      </header>
      
      <div class="flex-grow overflow-y-auto p-8 max-w-3xl mx-auto w-full">
        <NoteEditor />
      </div>
    </main>

    <!-- Right Panel (Agent Insights) -->
    <aside class="w-80 flex-shrink-0 z-10 p-4 hidden lg:block">
      <AgentPanel />
    </aside>
  </div>
</template>

<script setup lang="ts">
import GlassPanel from './components/GlassPanel.vue';
import EntryRow from './components/EntryRow.vue';
import AgentPanel from './components/AgentPanel.vue';
import NoteEditor from './components/NoteEditor.vue';
import { PlusIcon, ClockIcon, CalendarIcon, EllipsisHorizontalIcon } from '@heroicons/vue/24/outline';
</script>
