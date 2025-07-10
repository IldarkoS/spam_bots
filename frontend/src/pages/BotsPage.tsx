import React from 'react'
import { useEffect, useState } from 'react'
import { BotCard } from '@/components/BotCard'
import { getBots, deleteBot } from '@/api/bots'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

export default function BotsPage() {
  const [bots, setBots] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchBots = async () => {
      try {
        const data = await getBots()
        setBots(data)
      } catch (error) {
        console.error('Ошибка загрузки ботов:', error)
      }
    }

    fetchBots()
  }, [])

  const handleDelete = async (id) => {
    if (!window.confirm('Вы уверены, что хотите удалить этого бота?')) return

    try {
      await deleteBot(id)
      setBots((prev) => prev.filter((bot) => bot.id !== id))
    } catch (error) {
      console.error('Ошибка при удалении бота:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">🤖 Мои Telegram Боты</h1>
          <Link
            to="/bot/new"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl transition-colors shadow-md"
          >
            ➕ Новый бот
          </Link>
        </div>

        {bots.length === 0 ? (
          <div className="bg-white p-8 rounded-xl shadow-md border border-gray-200 text-center">
            <p className="text-gray-500">Нет добавленных ботов</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {bots.map((bot) => (
              <BotCard key={bot.id} bot={bot} onDelete={() => handleDelete(bot.id)} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}