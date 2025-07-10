import { api } from './axios'

export const getTasks = async () => {
  const { data } = await api.get('/tasks/')
  return data
}

export const getTaskById = async (taskId: number) => {
  const { data } = await api.get(`/task/${taskId}/`)
  return data
}

export const createTask = async (payload: any) => {
  const { data } = await api.post('/task/', payload)
  return data
}

export const updateTask = async (taskId: number, payload: any) => {
  const { data } = await api.patch(`/task/${taskId}/`, payload)
  return data
}

export const deleteTask = async (taskId: number) => {
  await api.delete(`/task/${taskId}/`)
}