import React from 'react'
import { useState } from 'react'
import { createBot } from '@/api/bots'
import { useNavigate } from 'react-router-dom'

export default function NewBotPage() {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    api_id: '',
    api_hash: '',
  })

  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const isFormValid = () => {
    return (
      formData.name.trim() !== '' &&
      formData.phone.trim() !== '' &&
      formData.api_id.trim() !== '' &&
      !isNaN(Number(formData.api_id)) &&
      formData.api_hash.trim() !== ''
    )
  }

  const handleSubmit = async () => {
    if (!isFormValid() || loading) return

    setLoading(true)
    try {
      const newBot = await createBot({
        ...formData,
        api_id: Number(formData.api_id),
      })
      navigate(`/bot/${newBot.id}`)
    } catch (error) {
      console.error('Ошибка при создании бота:', error)
      alert('Не удалось создать бота')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-200">
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white">
          <h1 className="text-2xl font-bold">➕ Новый Telegram Бот</h1>
          <p className="text-sm opacity-90">Заполните данные для подключения</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Имя бота */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">Имя бота</label>
            <input
              type="text"
              name="name"
              placeholder="Например: MyTelegramBot"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow"
            />
          </div>

          {/* Телефон */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">Телефон</label>
            <input
              type="text"
              name="phone"
              placeholder="+79991234567"
              value={formData.phone}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow"
            />
          </div>

          {/* API ID */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">API ID</label>
            <input
              type="text"
              name="api_id"
              placeholder="12345678"
              value={formData.api_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow"
            />
          </div>

          {/* API Hash */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">API Hash</label>
            <input
              type="text"
              name="api_hash"
              placeholder="a1b2c3d4e5f6g7h8i9j0k"
              value={formData.api_hash}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow"
            />
          </div>

          {/* Кнопка отправки */}
          <button
            onClick={handleSubmit}
            disabled={!isFormValid() || loading}
            className={`w-full mt-4 px-4 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-md font-medium ${
              isFormValid() && !loading
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                : 'bg-gray-200 text-gray-500 cursor-not-allowed'
            }`}
          >
            {loading ? 'Создание...' : '✅ Создать бота'}
          </button>
        </div>
      </div>
    </div>
  )
}