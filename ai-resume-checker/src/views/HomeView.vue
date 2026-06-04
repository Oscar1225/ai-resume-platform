<template>
  <div class="home-container">
    <div class="hero-section text-center">
      <h1 class="title">次世代 AI 職涯發展與招募平台</h1>
      <p class="subtitle">從履歷優化到模擬面試，讓 AI 成為您的專屬職涯顧問與精準招募夥伴。</p>
      <el-button type="primary" size="large" @click="startNow">立即開始使用</el-button>
    </div>

    <el-divider content-position="center">求職者專屬四大功能</el-divider>

    <!-- 網格排列展示四大功能 -->
    <el-row :gutter="20" class="features-row">
      <el-col :span="12" v-for="feature in features" :key="feature.title">
        <el-card shadow="hover" class="feature-card">
          <div class="icon">{{ feature.icon }}</div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const features = [
  { icon: '📝', title: 'AI 分析履歷', desc: '上傳 PDF，AI 立即為您的履歷健檢並給予優化建議。' },
  { icon: '✍️', title: 'AI 履歷撰寫', desc: '輸入基本經歷，AI 根據 STAR 原則為您生成專業履歷段落。' },
  { icon: '🎯', title: 'AI 職缺媒合', desc: '智能比對您的履歷與企業職缺，精準計算錄取適配度。' },
  { icon: '🎤', title: 'AI 模擬面試', desc: '與 AI 面試官進行即時對答，獲得專業反饋與修正建議。' }
];

const startNow = () => {
  if (authStore.isLogin) {
    router.push(`/dashboard/${authStore.role}`);
  } else {
    router.push('/login');
  }
};
</script>

<style scoped>
.hero-section { margin-bottom: 50px; padding: 40px 0; }
.title { font-size: 2.5rem; color: #303133; margin-bottom: 20px; }
.subtitle { font-size: 1.2rem; color: #606266; margin-bottom: 30px; }
.text-center { text-align: center; }
.feature-card { text-align: center; margin-bottom: 20px; height: 180px; }
.icon { font-size: 3rem; margin-bottom: 15px; }
</style>