<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold">Notes</h2>
      <button @click="notesStore.createNote()" class="p-2 rounded hover:bg-gray-300">+</button>
    </div>
    <ul>
      <li
        v-for="note in notesStore.notes"
        :key="note.id"
        @click="notesStore.selectNote(note.id)"
        class="cursor-pointer p-2 hover:bg-gray-200 rounded mb-2"
        :class="{ 'bg-gray-300': note.id === notesStore.selectedNoteId }"
      >
        <div class="font-bold">{{ note.title }}</div>
        <div class="flex flex-wrap mt-1">
          <span
            v-for="tag in note.tags"
            :key="tag"
            class="bg-blue-100 text-blue-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded"
          >
            {{ tag }}
          </span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useNotesStore } from '@/stores/notes';

const notesStore = useNotesStore();
</script>