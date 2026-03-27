import { create } from 'zustand'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  executionResults?: any
  timing?: any
  isLoading?: boolean
  error?: string
}

export interface ChatState {
  messages: Message[]
  isInitialized: boolean
  isLoading: boolean
  isInitializing: boolean
  addMessage: (message: Message) => void
  updateMessage: (id: string, updates: Partial<Message>) => void
  clearMessages: () => void
  setInitialized: (value: boolean) => void
  setLoading: (value: boolean) => void
  setInitializing: (value: boolean) => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isInitialized: false,
  isLoading: false,
  isInitializing: false,
  
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
  
  updateMessage: (id, updates) =>
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === id ? { ...msg, ...updates } : msg
      ),
    })),
  
  clearMessages: () =>
    set({ messages: [] }),
  
  setInitialized: (value) =>
    set({ isInitialized: value }),
  
  setLoading: (value) =>
    set({ isLoading: value }),
  
  setInitializing: (value) =>
    set({ isInitializing: value }),
}))
