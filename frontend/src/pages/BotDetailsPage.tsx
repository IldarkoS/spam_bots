import React from 'react'
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  getBot,
  requestCode,
  submitCode,
  submitPassword,
  runBot,
  stopBot,
} from '@/api/bots'
import { toast } from 'react-toastify'

export default function BotDetailsPage() {
  const { id } = useParams()
  const botId = Number(id)
  const navigate = useNavigate()
  const [bot, setBot] = useState<any>(null)
  const [code, setCode] = useState('')
  const [password, setPassword] = useState('')

  useEffect(() => {
    const fetchBot = async () => {
      try {
        const data = await getBot(botId)
        setBot(data)
      } catch (error) {
        toast.error('Ошибка загрузки бота')
        navigate('/')
      }
    }

    fetchBot()
  }, [botId, navigate])

  if (!bot) return <div className="p-4 text-gray-500">Загрузка...</div>

  const handleRequestCode = async () => {
    try {
      await requestCode(botId)
      toast.info('Код отправлен в Telegram')
      const updatedBot = await getBot(botId)
      setBot(updatedBot)
    } catch (error) {
      toast.error('Не удалось запросить код')
    }
  }

  const handleSendCode = async () => {
    if (!code.trim()) return
    try {
      await submitCode(botId, code)
      toast.success('Код успешно отправлен!')
      const updatedBot = await getBot(botId)
      setBot(updatedBot)
    } catch (error) {
      toast.error('Ошибка при отправке кода')
    }
  }

  const handleSendPassword = async () => {
    if (!password.trim()) return
    try {
      await submitPassword(botId, password)
      toast.success('Пароль успешно отправлен!')
      const updatedBot = await getBot(botId)
      setBot(updatedBot)
    } catch (error) {
      toast.error('Ошибка при отправке пароля')
    }
  }

  const handleRun = async () => {
    try {
      await runBot(botId)
      toast.success(`Бот "${bot.name}" запущен`)
      const updatedBot = await getBot(botId)
      setBot(updatedBot)
    } catch (error) {
      toast.error('Ошибка при запуске бота')
    }
  }

  const handleStop = async () => {
    try {
      await stopBot(botId)
      toast.success(`Бот "${bot.name}" остановлен`)
      const updatedBot = await getBot(botId)
      setBot(updatedBot)
    } catch (error) {
      toast.error('Ошибка при остановке бота')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-200">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-8 text-white">
          <h1 className="text-3xl font-bold">{bot.name}</h1>
          <p className="text-sm opacity-90">Телефон: {bot.phone}</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Status */}
          <div className="flex items-center gap-2">
            {bot.is_authorized ? (
              <>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                     className="text-green-500">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span className="text-green-700 font-medium">Авторизован</span>
              </>
            ) : (
              <>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                     className="text-red-500">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <span className="text-red-700 font-medium">Не авторизован</span>
              </>
            )}
          </div>

          {/* Auth Actions */}
          {!bot.is_authorized && (
            <div className="space-y-6">
              <button
                onClick={handleRequestCode}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white border border-gray-300 rounded-xl text-gray-700 font-medium hover:bg-gray-50 transition-all duration-200"
              >
                📨 Запросить код
              </button>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Введите код
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="123456"
                      value={code}
                      onChange={(e) => setCode(e.target.value)}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow"
                    />
                    <button
                      onClick={handleSendCode}
                      disabled={!code.trim()}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      📥 Отправить
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Введите пароль
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      placeholder="••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow"
                    />
                    <button
                      onClick={handleSendPassword}
                      disabled={!password.trim()}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      🔐 Отправить
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Control Buttons */}
          <div className="pt-4 border-t border-gray-200">
            <h2 className="text-lg font-semibold mb-4">Управление ботом</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                onClick={handleRun}
                disabled={!bot.is_authorized}
                className={`flex items-center justify-center gap-2 px-4 py-3 ${
                  bot.is_authorized
                    ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:from-green-600 hover:to-emerald-600'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                } rounded-xl transition-all duration-200 shadow-md`}
              >
                ▶️ Запустить
              </button>
              <button
                onClick={handleStop}
                disabled={!bot.is_authorized}
                className={`flex items-center justify-center gap-2 px-4 py-3 ${
                  bot.is_authorized
                    ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white hover:from-red-600 hover:to-pink-600'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                } rounded-xl transition-all duration-200 shadow-md`}
              >
                ⏹ Остановить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}