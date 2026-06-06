import axios from 'axios';

// 建立 Axios 實例，設定後端伺服器的網址
const api = axios.create({
  baseURL: 'https://ai-resume-api-nb9h.onrender.com/v1', // FastAPI 的預設位址//https://ai-resume-api-nb9h.onrender.com
  timeout: 30000, // 設定較長的超時時間，因為未來 AI 處理需要時間//http://127.0.0.1:8000/v1
});
// 🛡️ 新增：Axios 請求攔截器 (Request Interceptor)
api.interceptors.request.use(
  (config) => {
    // 每次打 API 前，都去 localStorage 找找看有沒有 Token
    const token = localStorage.getItem('token');
    
    // 如果有 Token，就把它強制塞進這次請求的 Header 裡
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
// 封裝上傳履歷的 API
export const uploadResume = async (file) => {
  try {
    const formData = new FormData();
    formData.append('resume_file', file); 
    
    const response = await api.post('/resume/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data; 
  } catch (error) {
    console.error('API 呼叫失敗:', error);
    throw error;
  }
};
// 註冊 API
export const registerUser = async (email, password, role) => {
  try {
    const response = await api.post('/auth/register', { email, password, role });
    return response.data;
  } catch (error) {
    // 拋出後端回傳的錯誤訊息 (例如: Email 已註冊)
    throw error.response?.data?.detail || '註冊失敗';
  }
};

// 登入 API
export const loginUser = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || '登入失敗';
  }
};

export default api;