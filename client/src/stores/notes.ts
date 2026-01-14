import { defineStore } from 'pinia';

export interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: Date;
  updatedAt: Date;
  tags: string[];
}

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: [
      { id: '1', title: 'Meeting Notes', content: '<p>This is a note about the meeting.</p>', createdAt: new Date(), updatedAt: new Date(), tags: ['work', 'meeting'] },
      { id: '2', title: 'Grocery List', content: '<ul><li>Milk</li><li>Bread</li><li>Cheese</li></ul>', createdAt: new Date(), updatedAt: new Date(), tags: ['personal', 'shopping'] },
      { id: '3', title: 'Workout Plan', content: '<p>3x10 squats</p><p>3x10 bench press</p>', createdAt: new Date(), updatedAt: new Date(), tags: ['health', 'fitness'] },
    ] as Note[],
    selectedNoteId: null as string | null,
  }),
  getters: {
    selectedNote: (state) => {
      if (!state.selectedNoteId) return null;
      return state.notes.find(note => note.id === state.selectedNoteId);
    },
  },
  actions: {
    selectNote(id: string) {
      this.selectedNoteId = id;
    },
    updateNote(id: string, title: string, content: string) {
      const note = this.notes.find(note => note.id === id);
      if (note) {
        note.title = title;
        note.content = content;
        note.updatedAt = new Date();
      }
    },
    createNote() {
      const newNote: Note = {
        id: Date.now().toString(),
        title: 'New Note',
        content: '',
        createdAt: new Date(),
        updatedAt: new Date(),
        tags: [],
      };
      this.notes.unshift(newNote);
      this.selectedNoteId = newNote.id;
    },
  },
});
