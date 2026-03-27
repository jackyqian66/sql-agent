'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Play, RefreshCw } from 'lucide-react'
import { motion } from 'framer-motion'

interface ChatInputProps {
  onSend: (message: string) => void
  onInit: () => void
  isLoading: boolean
  isInitialized: boolean
  isInitializing: boolean
}

export default function ChatInput({ 
  onSend, 
  onInit, 
  isLoading, 
  isInitialized,
  isInitializing 
}: ChatInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px'
    }
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isLoading) {
      onSend(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const quickQuestions = [
    '2024年第三季度的总销售额是多少？',
    '显示所有销售数据',
    '我们有多少客户？',
  ]

  return (
    <div className="border-t border-border glass">
      <div className="max-w-3xl mx-auto px-6 py-5">
        {!isInitialized ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: 'spring', stiffness: 100 }}
            className="text-center"
          >
            <p className="text-muted/80 mb-5 text-lg">
              请先初始化 Agent 以连接数据库
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onInit}
              disabled={isInitializing}
              className="glass-button px-10 py-4 rounded-2xl font-semibold inline-flex items-center gap-3 shadow-xl shadow-primary/30"
            >
              {isInitializing ? (
                <>
                  <RefreshCw className="w-6 h-6 animate-spin" />
                  初始化中...
                </>
              ) : (
                <>
                  <Play className="w-6 h-6" />
                  初始化 Agent
                </>
              )}
            </motion.button>
          </motion.div>
        ) : (
          <>
            {!isLoading && (
              <div className="flex flex-wrap gap-3 mb-5">
                {quickQuestions.map((q, idx) => (
                  <motion.button
                    key={idx}
                    initial={{ opacity: 0, y: 10, scale: 0.9 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ delay: idx * 0.1, type: 'spring', stiffness: 200 }}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => onSend(q)}
                    className="glass-button-secondary px-5 py-3 rounded-xl text-sm font-medium hover:bg-card-hover transition-all duration-300 shadow-sm"
                  >
                    {q}
                  </motion.button>
                ))}
              </div>
            )}
            
            <form onSubmit={handleSubmit} className="relative">
              <motion.div
                whileHover={{ scale: 1.01 }}
                className="glass-card rounded-3xl p-3 flex items-end gap-3 shadow-2xl"
              >
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="输入您的查询..."
                  disabled={isLoading}
                  className="flex-1 bg-transparent border-none outline-none resize-none px-5 py-3 min-h-[60px] max-h-[200px] disabled:opacity-50 text-lg"
                  rows={1}
                />
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="glass-button p-4 rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary/30"
                >
                  {isLoading ? (
                    <RefreshCw className="w-6 h-6 animate-spin" />
                  ) : (
                    <Send className="w-6 h-6" />
                  )}
                </motion.button>
              </motion.div>
            </form>
          </>
        )}
      </div>
    </div>
  )
}
