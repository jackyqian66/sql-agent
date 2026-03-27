import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SQL Agent - 智能数据库查询助手',
  description: '基于AI的智能数据库查询助手，支持自然语言查询SQL数据库',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}
