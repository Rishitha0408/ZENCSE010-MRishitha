import axios from 'axios'

/**
 * Axios instance for the Admin Dashboard.
 */
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor to attach API key
apiClient.interceptors.request.use((config) => {
  const apiKey = process.env.REACT_APP_API_KEY || 'default_api_key_for_dev_only'
  if (apiKey) {
    config.headers['X-API-Key'] = apiKey
  }
  return config
})

// Response interceptor for consistent error handling and data unwrapping
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      const { status, data } = error.response

      if (status === 401) {
        alert('Invalid API Key. Please check your configuration.')
        // Potential redirect to config page: window.location.href = '/config'
      } else if (status === 422) {
        // Return error data so forms can show field-level validation errors
        return Promise.reject(data)
      } else {
        const message = data.error || 'An unexpected error occurred'
        console.error(`API Error (${status}):`, message)
        return Promise.reject(new Error(message))
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
