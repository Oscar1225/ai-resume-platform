<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <h2 class="text-center mb-4">建立新帳號</h2>
      
      <el-form @submit.prevent="handleRegister" label-position="top">
        <el-form-item label="電子信箱">
          <el-input v-model="form.email" placeholder="請輸入電子信箱" size="large" required type="email" />
        </el-form-item>
        
        <el-form-item label="設定密碼">
          <el-input v-model="form.password" placeholder="請輸入密碼" type="password" size="large" show-password required />
        </el-form-item>

        <el-form-item label="確認密碼">
          <el-input v-model="form.confirmPassword" placeholder="請再次輸入密碼" type="password" size="large" show-password required />
        </el-form-item>
        
        <el-form-item label="您要註冊的身分是？">
          <el-select v-model="form.role" style="width: 100%;" size="large">
            <el-option label="一般求職者 (User)" value="user" />
            <el-option label="企業徵才 (Company)" value="company" />
          </el-select>
        </el-form-item>

        <el-button type="primary" size="large" class="w-100 mt-3" native-type="submit" :loading="isLoading">
          立即註冊
        </el-button>
      </el-form>

      <div class="register-link text-center mt-4">
        <span>已經有帳號了嗎？</span>
        <el-button type="primary" link @click="$router.push('/login')">返回登入</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { registerUser } from '../api';
import { ElMessage } from 'element-plus';

const router = useRouter();
const isLoading = ref(false);

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  role: 'user'
});

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    ElMessage.error('兩次輸入的密碼不一致！');
    return;
  }

  isLoading.value = true;
  try {
    await registerUser(form.email, form.password, form.role);
    ElMessage.success('註冊成功！請登入您的帳號。');
    router.push('/login'); // 註冊成功後導回登入頁
  } catch (error) {
    ElMessage.error(error); // 顯示後端傳來的錯誤 (例如信箱重複)
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 樣式與 LoginView 共用 */
.login-container { display: flex; justify-content: center; align-items: center; min-height: 70vh; padding: 20px;}
.login-card { width: 100%; max-width: 400px; padding: 20px; border-radius: 12px; }
.text-center { text-align: center; }
.w-100 { width: 100%; }
.mt-3 { margin-top: 15px; }
.mt-4 { margin-top: 25px; }
.mb-4 { margin-bottom: 25px; }
.register-link { font-size: 0.9rem; color: #606266; border-top: 1px solid #ebeef5; padding-top: 15px; }
</style>