import React from 'react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getTasks, deleteTask } from '@/api/tasks'

export default function TasksPage() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await getTasks()
        setTasks(data)
      } catch (error) {
        console.error('Ошибка загрузки задач:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [])

  const handleDelete = async (taskId) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту задачу?')) return

    try {
      await deleteTask(taskId)
      setTasks((prev) => prev.filter((task) => task.id !== taskId))
    } catch (error) {
      console.error('Ошибка при удалении задачи:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Загрузка...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">📋 Задачи</h1>
          <Link
            to="/task/new"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl transition-colors shadow-md"
          >
            ➕ Новая задача
          </Link>
        </div>

        {tasks.length === 0 ? (
          <div className="bg-white p-8 rounded-xl shadow-md border border-gray-200 text-center">
            <p className="text-gray-500">Нет активных задач</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-xl shadow-md border border-gray-200 p-6 space-y-4"
              >
                <h2 className="text-xl font-semibold">{task.channel}</h2>
                <p className="text-sm text-gray-600">ID: {task.id}</p>
                <p className="text-sm text-gray-600">Статус: {task.status}</p>
                <p className="text-sm text-gray-600">Тип: {task.scope}</p>
                {task.bot_id && (
                  <p className="text-sm text-gray-600">Бот ID: {task.bot_id}</p>
                )}

                {/* Кнопки управления */}
                <div className="pt-4 border-t border-gray-200 flex justify-between gap-2">
                  <Link
                    to={`/task/edit/${task.id}`}
                    className="flex-1 px-4 py-2 bg-indigo-100 text-indigo-700 hover:bg-indigo-200 rounded-lg transition-colors text-center"
                  >
                    ✏️ Редактировать
                  </Link>
                  <button
                    onClick={() => handleDelete(task.id)}
                    className="flex-1 px-4 py-2 bg-red-100 text-red-700 hover:bg-red-200 rounded-lg transition-colors"
                  >
                    🗑 Удалить
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}