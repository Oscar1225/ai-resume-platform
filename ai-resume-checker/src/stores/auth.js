import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '../api'; // 引入 api，以便設定全局 Token

export const useAuthStore = defineStore('auth', () => {
  // 從 localStorage 讀取初始狀態
  const isLogin = ref(!!localStorage.getItem('token'));
  const role = ref(localStorage.getItem('role') || '');
  const token = ref(localStorage.getItem('token') || '');

  // 登入成功時呼叫
  const login = (authData) => {
    isLogin.value = true;
    role.value = authData.role;
    token.value = authData.access_token;
    
    // 存入瀏覽器
    localStorage.setItem('token', authData.access_token);
    localStorage.setItem('role', authData.role);
  };

  // 登出時呼叫
  const logout = () => {
    isLogin.value = false;
    role.value = '';
    token.value = '';
    
    localStorage.removeItem('token');
    localStorage.removeItem('role');
  };

  return { isLogin, role, token, login, logout };
});