<template>
  <div class="app-wrapper">
    <!-- 頂部導覽列 -->
    <el-menu mode="horizontal" :default-active="$route.path" router class="nav-menu">
      <el-menu-item index="/">
        <span class="logo-text">🚀 AI 職涯媒合平台</span>
      </el-menu-item>
      
      <div class="flex-grow" /> 
      
      <!-- 未登入狀態 -->
      <template v-if="!authStore.isLogin">
        <el-menu-item index="/">平台介紹</el-menu-item>
        <el-menu-item index="/login">
          <el-button type="primary" round>登入 / 註冊</el-button>
        </el-menu-item>
      </template>

      <!-- 已登入狀態 -->
      <template v-else>
        <el-menu-item :index="`/dashboard/${authStore.role}`">進入控制台</el-menu-item>
        <el-menu-item @click="handleLogout">登出</el-menu-item>
      </template>
    </el-menu>

    <!-- 核心內容區塊 -->
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  ElMessage.success('已成功登出');
  router.push('/'); // 登出後導回首頁
};
</script>

<style>
body {
  margin: 0;
  background-color: #f5f7fa; 
  font-family: sans-serif;
}
.app-wrapper { min-height: 100vh; display: flex; flex-direction: column; }
.nav-menu { padding: 0 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.logo-text { font-size: 1.2rem; font-weight: bold; color: #409EFF; }
.flex-grow { flex-grow: 1; }
body {
  margin: 0;
  background-color: #f5f7fa; 
  font-family: sans-serif;
}
.app-wrapper { min-height: 100vh; display: flex; flex-direction: column; }

/* 確保頂部導覽列在最上層，不會被側邊欄蓋住 */
.nav-menu { padding: 0 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); z-index: 100; position: relative; }
.logo-text { font-size: 1.2rem; font-weight: bold; color: #409EFF; }
.flex-grow { flex-grow: 1; }

/* 🛑 核心修改：移除 max-width 和 margin，讓控制台能向外延展填滿螢幕 */
.main-content { 
  flex: 1; 
  width: 100%; 
  display: flex; 
  flex-direction: column; 
}
</style>