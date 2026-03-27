'use client'

import { motion } from 'framer-motion'
import { Database, Zap, RefreshCcw } from 'lucide-react'

export default function Header({ isInitialized }: { isInitialized: boolean }) {
  const handleClearHistory = () => {
    window.location.reload()
  }

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass border-b border-border sticky top-0 z-50"
      style={{
        boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
      }}
    >
      <div className="max-w-5xl mx-auto px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <motion.div
                whileHover={{ scale: 1.05, rotate: 5 }}
                className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center shadow-lg shadow-primary/30"
              >
                <Database className="w-7 h-7 text-white" />
              </motion.div>
              {isInitialized && (
                <motion.div
                  layoutId="status-dot"
                  className="absolute -right-1 -bottom-1 w-4 h-4 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full border-3 border-background shadow-lg shadow-green-500/50"
                  animate={{ 
                    scale: [1, 1.3, 1],
                    boxShadow: [
                      '0 0 0 0 rgba(16, 185, 129, 0.4)',
                      '0 0 0 8px rgba(16, 185, 129, 0)',
                      '0 0 0 0 rgba(16, 185, 129, 0)'
                    ]
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
              )}
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-white via-primary to-accent bg-clip-text text-transparent">
                SQL Agent
              </h1>
              <p className="text-xs text-muted/80 mt-0.5">智能数据库查询助手</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleClearHistory}
              className="glass-button-secondary px-5 py-2.5 rounded-xl text-sm font-medium flex items-center gap-2 hover:bg-card-hover transition-all duration-300 shadow-sm"
            >
              <RefreshCcw className="w-4.5 h-4.5" />
              <span>清空历史</span>
            </motion.button>
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium backdrop-blur-sm ${
              isInitialized 
                ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-300 border border-green-500/40 shadow-lg shadow-green-500/20' 
                : 'bg-gradient-to-r from-yellow-500/20 to-amber-500/20 text-yellow-300 border border-yellow-500/40 shadow-lg shadow-yellow-500/20'
            }`}>
              <Zap className="w-4.5 h-4.5" />
              <span>{isInitialized ? '已连接' : '未初始化'}</span>
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  )
}
