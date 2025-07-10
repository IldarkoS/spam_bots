import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Header } from '@/components/Header'
import BotsPage from './pages/BotsPage'
import BotDetailsPage from './pages/BotDetailsPage'
import TasksPage from './pages/TasksPage'
import NewTaskPage from './pages/NewTaskPage'
import NewBotPage from './pages/NewBotPage'
import EditTaskPage from './pages/EditTaskPage'

export default function App() {
  return (
    <>
      <Header />
      <main className="container mx-auto px-6 py-8">
        <Routes>
          <Route path="/" element={<BotsPage />} />
          <Route path="/bot/:id" element={<BotDetailsPage />} />
          <Route path="/bot/new" element={<NewBotPage />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/task/new" element={<NewTaskPage />} />
          <Route path="/task/edit/:id" element={<EditTaskPage />} />
        </Routes>
      </main>
    </>
  )
}