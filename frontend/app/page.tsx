'use client'

import { useEffect } from 'react'
import Header from '@/components/Header'
import MessageList from '@/components/MessageList'
import ChatInput from '@/components/ChatInput'
import { useChatStore, Message } from '@/store/useChatStore'
import { initializeAgent, sendQuery } from '@/lib/api'

export default function Home() {
  const {
    messages,
    isInitialized,
    isLoading,
    isInitializing,
    addMessage,
    updateMessage,
    setInitialized,
    setLoading,
    setInitializing,
  } = useChatStore()

  useEffect(() => {
    if (!isInitialized && !isInitializing) {
      handleInit()
    }
  }, [isInitialized, isInitializing])

  const handleInit = async () => {
    setInitializing(true)
    try {
      const result = await initializeAgent('./data')
      if (result.success) {
        setInitialized(true)
      } else {
        alert(result.error || '初始化失败')
      }
    } catch (error) {
      alert('初始化失败: ' + (error as Error).message)
    } finally {
      setInitializing(false)
    }
  }

  const handleSend = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    }
    addMessage(userMessage)

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isLoading: true,
    }
    addMessage(assistantMessage)
    setLoading(true)

    try {
      const history = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }))
      
      const result = await sendQuery(content, history)
      if (result.success) {
        updateMessage(assistantMessage.id, {
          content: result.response || '已完成查询',
          isLoading: false,
          executionResults: result.execution_results,
          timing: result.timing,
        })
      } else {
        updateMessage(assistantMessage.id, {
          content: '抱歉，处理您的查询时出错了。',
          isLoading: false,
          error: result.error,
        })
      }
    } catch (error) {
      updateMessage(assistantMessage.id, {
        content: '抱歉，处理您的查询时出错了。',
        isLoading: false,
        error: (error as Error).message,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col">
      <Header isInitialized={isInitialized} />
      <main className="flex-1 flex flex-col overflow-hidden">
        <MessageList messages={messages} />
        <div className="flex-shrink-0">
          <ChatInput
            onSend={handleSend}
            onInit={handleInit}
            isLoading={isLoading}
            isInitialized={isInitialized}
            isInitializing={isInitializing}
          />
        </div>
      </main>
    </div>
  )
}
