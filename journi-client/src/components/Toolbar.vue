<template>
  <div class="flex items-center p-2 border-b">
    <button @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }" class="p-2">
      Bold
    </button>
    <button @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }" class="p-2">
      Italic
    </button>
    <button @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }" class="p-2">
      Strike
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }" class="p-2">
      H1
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }" class="p-2">
      H2
    </button>
    <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }" class="p-2">
      Bullet List
    </button>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { Editor } from '@tiptap/vue-3';

defineProps<{
  editor: Editor;
}>();
</script>

<style>
.is-active {
  font-weight: bold;
  background-color: #e0e0e0;
}
</style>
