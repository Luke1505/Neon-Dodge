import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Neon Dodge - Indie Game',
  description: 'A neon-themed dodge game with power-ups and combo system',
  keywords: ['game', 'neon', 'dodge', 'indie', 'web game'],
  authors: [{ name: 'Luke1505' }],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-mono">
        {children}
      </body>
    </html>
  )
}