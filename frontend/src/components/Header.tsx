import React from 'react'
import { Link, useLocation } from 'react-router-dom'

export const Header = () => {
  const location = useLocation()

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-semibold text-indigo-700">
          Bot Manager
        </Link>

        <nav>
          <ul className="flex space-x-6 text-sm font-medium">
            <li>
              <Link
                to="/"
                className={`transition-colors ${
                  location.pathname === '/' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600'
                }`}
              >
                Боты
              </Link>
            </li>
            <li>
              <Link
                to="/tasks"
                className={`transition-colors ${
                  location.pathname === '/tasks' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600'
                }`}
              >
                Задачи
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  )
}