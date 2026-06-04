<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <h2 class="text-center mb-4">歡迎使用平台</h2>
      
      <el-form @submit.prevent="handleLogin" label-position="top">
        <el-form-item label="電子信箱">
          <el-input v-model="email" placeholder="請輸入電子信箱" size="large" required type="email" />
        </el-form-item>
        <el-form-item label="密碼">
          <el-input v-model="password" placeholder="請輸入密碼" type="password" size="large" show-password required />
        </el-form-item>

        <el-button type="primary" size="large" class="w-100 mt-3" native-type="submit" :loading="isLoading">
          登入
        </el-button>
      </el-form>

      <div class="register-link text-center mt-4">
        <span>還沒有帳號嗎？</span>
        <el-button type="primary" link @click="$router.push('/register')">立即註冊</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { loginUser } from '../api';
import { ElMessage } from 'element-plus';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  try {
    // 1. 呼叫後端 API
    const response = await loginUser(email.value, password.value);
    
    // 2. 將回傳的 token 與 role 存入 Pinia
    authStore.login(response);
    ElMessage.success(`登入成功！`);
    
    // 3. 根據後端回傳的角色，引導至對應的頁面
    if (response.role === 'user') {
      router.push('/dashboard/user');
    } else if (response.role === 'company') {
      router.push('/dashboard/company');
    } else if (response.role === 'admin') {
      router.push('/dashboard/admin');
    }
  } catch (error) {
    ElMessage.error(error); // 顯示帳號密碼錯誤
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 與上方 RegisterView 共用相同樣式即可 */
.login-container { display: flex; justify-content: center; align-items: center; min-height: 70vh; padding: 20px;}
.login-card { width: 100%; max-width: 400px; padding: 20px; border-radius: 12px; }
.text-center { text-align: center; }
.w-100 { width: 100%; }
.mt-3 { margin-top: 15px; }
.mt-4 { margin-top: 25px; }
.mb-4 { margin-bottom: 25px; }
.register-link { font-size: 0.9rem; color: #606266; border-top: 1px solid #ebeef5; padding-top: 15px; }
</style>