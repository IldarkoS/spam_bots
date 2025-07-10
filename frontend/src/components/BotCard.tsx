import React from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { CheckCircle, Lock, Play, Square, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import {
  runBot as apiRunBot,
  stopBot as apiStopBot,
} from '@/api/bots'

export const BotCard = ({ bot, onDelete }) => {
  const navigate = useNavigate()

  const handleRun = async () => {
    try {
      await apiRunBot(bot.id)
      window.location.reload()
    } catch (error) {
      console.error('Ошибка при запуске бота:', error)
    }
  }

  const handleStop = async () => {
    try {
      await apiStopBot(bot.id)
      window.location.reload()
    } catch (error) {
      console.error('Ошибка при остановке бота:', error)
    }
  }

  return (
    <Card className="overflow-hidden border border-gray-200 bg-white shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-6 space-y-4">
        {/* Заголовок */}
        <div>
          <h2 className="text-xl font-semibold">{bot.name}</h2>
          <p className="text-sm text-gray-600 mt-1">Телефон: {bot.phone}</p>
        </div>

        {/* Статус авторизации */}
        <div className="flex items-center gap-2">
          {bot.is_authorized ? (
            <>
              <CheckCircle className="text-green-500" size={18} />
              <span className="text-green-700 font-medium">Авторизован</span>
            </>
          ) : (
            <>
              <Lock className="text-red-500" size={18} />
              <span className="text-red-700 font-medium">Не авторизован</span>
            </>
          )}
        </div>

        {/* Статус работы бота */}
        <div className="flex items-center gap-2">
          {bot.is_active ? (
            <>
              <Play className="text-blue-500" size={18} />
              <span className="text-blue-700 font-medium">Работает</span>
            </>
          ) : (
            <>
              <Square className="text-gray-500" size={18} />
              <span className="text-gray-700 font-medium">Остановлен</span>
            </>
          )}
        </div>

        {/* Кнопки управления */}
        <div className="pt-4 border-t border-gray-200 space-y-3">
          <button
            onClick={() => navigate(`/bot/${bot.id}`)}
            className="w-full text-left px-4 py-2 bg-indigo-100 text-indigo-700 hover:bg-indigo-200 rounded-lg transition-colors"
          >
            Подробнее
          </button>



          {/* Кнопка удаления */}
          <button
            onClick={onDelete}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-red-600 hover:text-red-800 transition-colors"
          >
            <Trash2 size={18} />
            <span>Удалить</span>
          </button>
        </div>
      </CardContent>
    </Card>
  )
}