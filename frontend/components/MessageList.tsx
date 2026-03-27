'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { User, Bot, Loader2 } from 'lucide-react'
import { Message } from '@/store/useChatStore'
import { useEffect, useRef } from 'react'

interface MessageListProps {
  messages: Message[]
}

export default function MessageList({ messages }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <motion.div
          initial={{ scale: 0.8, opacity: 0, rotate: -10 }}
          animate={{ scale: 1, opacity: 1, rotate: 0 }}
          transition={{ type: 'spring', stiffness: 200, damping: 15 }}
          className="w-32 h-32 mb-8 rounded-[2rem] bg-gradient-to-br from-primary/20 via-secondary/20 to-accent/20 flex items-center justify-center shadow-2xl shadow-primary/20"
        >
          <Bot className="w-16 h-16 text-primary" />
        </motion.div>
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 100 }}
        >
          <h2 className="text-3xl font-bold bg-gradient-to-r from-white via-primary to-accent bg-clip-text text-transparent">
            欢迎使用 SQL Agent
          </h2>
        </motion.div>
      </div>
    )
  }

  return (
    <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-8 space-y-8">
      <AnimatePresence>
        {messages.map((message, index) => (
          <motion.div
            key={message.id}
            initial={{ 
              x: message.role === 'user' ? 40 : -40, 
              opacity: 0,
              scale: 0.95
            }}
            animate={{ x: 0, opacity: 1, scale: 1 }}
            transition={{ 
              delay: index * 0.08,
              type: 'spring',
              stiffness: 200,
              damping: 20
            }}
            className={`flex gap-4 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <motion.div
              whileHover={{ scale: 1.1, rotate: message.role === 'user' ? 5 : -5 }}
              className={`flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center shadow-lg ${
                message.role === 'user'
                  ? 'bg-gradient-to-br from-primary to-secondary shadow-primary/30'
                  : 'bg-gradient-to-br from-accent to-primary shadow-accent/30'
              }`}
            >
              {message.role === 'user' ? (
                <User className="w-6 h-6 text-white" />
              ) : (
                <Bot className="w-6 h-6 text-white" />
              )}
            </motion.div>
            
            <div className={`max-w-2xl ${message.role === 'user' ? 'flex flex-col items-end' : ''}`}>
              <motion.div
                whileHover={{ scale: 1.01 }}
                className={`glass-card rounded-3xl px-6 py-5 shadow-xl ${
                  message.role === 'user' 
                    ? 'bg-gradient-to-br from-primary/25 to-secondary/25 border-primary/30' 
                    : 'border-accent/20'
                }`}
              >
                <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                
                {message.isLoading && (
                  <div className="flex items-center gap-3 mt-4 text-muted">
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span className="text-sm font-medium">思考中...</span>
                  </div>
                )}
                
                {message.error && (
                  <div className="mt-4 p-4 rounded-2xl bg-gradient-to-r from-red-500/10 to-rose-500/10 border border-red-500/30 text-red-300 text-sm">
                    {message.error}
                  </div>
                )}
              </motion.div>
              
              <div className="text-xs text-muted/60 mt-3 px-2">
                {message.timestamp.toLocaleTimeString('zh-CN')}
              </div>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
