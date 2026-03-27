const API_BASE = 'http://localhost:8000/api'

export interface ApiResponse<T = any> {
  success: boolean
  error?: string
  data?: T
  message?: string
  response?: string
  execution_results?: any
  timing?: any
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export async function healthCheck(): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE}/health`)
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Network error',
    }
  }
}

export async function initializeAgent(dataDirectory: string = './data'): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE}/init`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data_directory: dataDirectory }),
    })
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Network error',
    }
  }
}

export async function sendQuery(query: string, history: ChatMessage[] = []): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, history }),
    })
    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Network error',
    }
  }
}
