<template>
  <div class="p-4 h-full">
    <div v-if="selectedNote" class="h-full flex flex-col border rounded">
      <div class="flex justify-between items-center p-2 border-b">
        <input
          type="text"
          placeholder="Note title"
          class="w-full p-2"
          :value="selectedNote.title"
          @input="updateTitle"
        />
        <button @click="saveNote" class="bg-blue-500 text-white px-4 py-2 rounded ml-4">Save</button>
      </div>
      <Toolbar v-if="editor" :editor="editor" />
      <editor-content :editor="editor" class="flex-grow p-2" />
    </div>
    <div v-else class="h-full flex items-center justify-center text-gray-500">
      <p>Select a note to start editing</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch, onUnmounted } from 'vue';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import Toolbar from './Toolbar.vue';
import { useNotesStore } from '@/stores/notes';
import { storeToRefs } from 'pinia';
import axios from 'axios';

const notesStore = useNotesStore();
const { selectedNote } = storeToRefs(notesStore);

const editor = useEditor({
  extensions: [StarterKit],
  content: selectedNote.value?.content,
  onUpdate: ({ editor }) => {
    if (selectedNote.value) {
      notesStore.updateNote(selectedNote.value.id, selectedNote.value.title, editor.getHTML());
    }
  },
});

watch(selectedNote, (note) => {
  if (editor.value && note) {
    if (editor.value.getHTML() !== note.content) {
      editor.value.commands.setContent(note.content);
    }
  } else if (editor.value) {
    editor.value.commands.clearContent();
  }
});

const updateTitle = (event: Event) => {
  if (selectedNote.value) {
    const target = event.target as HTMLInputElement;
    notesStore.updateNote(selectedNote.value.id, target.value, selectedNote.value.content);
  }
};

const saveNote = async () => {
  if (selectedNote.value) {
    try {
      await axios.post('http://localhost:8000/api/entries', {
        id: selectedNote.value.id,
        title: selectedNote.value.title,
        content: editor.value?.getHTML(),
      });
      alert('Note saved!');
    } catch (error) {
      console.error('Error saving note:', error);
      alert('Failed to save note.');
    }
  }
};

onUnmounted(() => {
  editor.value?.destroy();
});
</script>
