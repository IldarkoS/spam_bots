import React from 'react'
import {useEffect, useState} from 'react'
import { useNavigate } from 'react-router-dom'
import { createTask } from '@/api/tasks'
import { getBots } from '@/api/bots'

export default function NewTaskPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    title: '',
    channel: '',
    scope: 'GLOBAL',
    bot_id: ''
  })
  const [bots, setBots] = useState([])

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

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const isFormValid = () => {
    if (!form.title || !form.channel) return false
    if (form.scope === 'PERSONAL' && !form.bot_id) return false
    return true
  }

  const handleSubmit = async () => {
    if (!isFormValid()) return

    try {
      await createTask({
        title: form.title,
        channel: form.channel,
        scope: form.scope,
        bot_id: form.scope === 'PERSONAL' ? Number(form.bot_id) : null,
      })
      navigate('/tasks')
    } catch (error) {
      console.error('Ошибка при создании задачи:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-lg mx-auto bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">📝 Новая задача</h1>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Название задачи</label>
          <input
            type="text"
            name="title"
            placeholder="Например: Парсинг канала"
            value={form.title}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Канал</label>
          <input
            type="text"
            name="channel"
            placeholder="@username"
            value={form.channel}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        {/* Scope */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Тип задачи</label>
          <select
            name="scope"
            value={form.scope}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          >
            <option value="GLOBAL">GLOBAL — для всех ботов</option>
            <option value="PERSONAL">PERSONAL — для конкретного бота</option>
          </select>
        </div>

        {form.scope === 'PERSONAL' && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Бот</label>
            <select
              name="bot_id"
              value={form.bot_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              <option value="">— Выберите бота —</option>
              {bots.map(bot => (
                <option key={bot.id} value={bot.id}>
                  {bot.name} ({bot.phone})
                </option>
              ))}
            </select>
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={!isFormValid()}
          className={`mt-6 w-full py-2 px-4 rounded-lg font-medium transition-colors ${
            isFormValid()
              ? 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white'
              : 'bg-gray-200 text-gray-500 cursor-not-allowed'
          }`}
        >
          ✅ Создать задачу
        </button>
      </div>
    </div>
  )
}