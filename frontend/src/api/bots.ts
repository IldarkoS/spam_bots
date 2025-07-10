import { api } from './axios'

export const getBots = async () => {
  const { data } = await api.get('/bots/')
  return data
}

export const getBot = async (id: number) => {
  const { data } = await api.get(`/bot/${id}/`)
  return data
}

export const createBot = async (payload) => {
  const { data } = await api.post('/bot/', payload)
  return data
}

export const requestCode = async (id: number) => {
  return api.post(`/bot/auth/request_code/${id}/`)
}

export const submitCode = async (id: number, code: string) => {
  return api.post(`/bot/auth/submit_code/${id}/`, { code })
}

export const submitPassword = async (id: number, password: string) => {
  return api.post(`/bot/auth/submit_password/${id}/`, { password })
}

export const runBot = async (id: number) => {
  return api.post(`/bot/run/${id}/`)
}

export const stopBot = async (id: number) => {
  return api.post(`/bot/stop/${id}/`)
}

export const deleteBot = async (id: number) => {
  return api.delete(`/bot/${id}/`)
}