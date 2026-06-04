<template>
  <div class="user-dashboard">
    <el-aside width="240px" class="desktop-sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">🚀</span>
        <span class="logo-text">AI 職涯平台</span>
      </div>
      <el-menu 
        :default-active="activeMenu" 
        @select="handleMenuSelect" 
        class="custom-menu"
      >
        <el-menu-item index="analysis">
          <span class="menu-icon">📝</span><span>AI 履歷健檢</span>
        </el-menu-item>
        <el-menu-item index="generator">
          <span class="menu-icon">✍️</span><span>AI 履歷撰寫</span>
        </el-menu-item>
        <el-menu-item index="matcher">
          <span class="menu-icon">🎯</span><span>AI 職缺媒合</span>
        </el-menu-item>
        <el-menu-item index="interview">
          <span class="menu-icon">🎤</span><span>AI 模擬面試</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-drawer 
      v-model="drawerVisible" 
      direction="ltr" 
      size="240px" 
      :with-header="false"
    >
      <div class="sidebar-logo">
        <span class="logo-icon">🚀</span>
        <span class="logo-text">AI 職涯平台</span>
      </div>
      <el-menu 
        :default-active="activeMenu" 
        @select="handleMenuSelect" 
        class="custom-menu"
      >
        <el-menu-item index="analysis">
          <span class="menu-icon">📝</span><span>AI 履歷健檢</span>
        </el-menu-item>
        <el-menu-item index="generator">
          <span class="menu-icon">✍️</span><span>AI 履歷撰寫</span>
        </el-menu-item>
        <el-menu-item index="matcher">
          <span class="menu-icon">🎯</span><span>AI 職缺媒合</span>
        </el-menu-item>
        <el-menu-item index="interview">
          <span class="menu-icon">🎤</span><span>AI 模擬面試</span>
        </el-menu-item>
      </el-menu>
    </el-drawer>

    <el-container class="main-container">
      
      <el-header class="dashboard-header">
        <div class="header-left">
          <el-button 
            class="menu-toggle" 
            text 
            @click="drawerVisible = true"
          >
            <span class="hamburger">☰</span>
          </el-button>
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        
        <div class="header-right">
          <el-avatar size="small" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
          <span class="user-greeting">求職者</span>
        </div>
      </el-header>

      <el-main class="dashboard-main">
        <transition name="fade-slide" mode="out-in">
          <component :is="currentComponent" />
        </transition>
      </el-main>
      
    </el-container>
  </div>
</template>

<script setup>
import { ref, shallowRef, computed } from 'vue';

// 引入 4 大功能元件
import ResumeUploader from '../components/ResumeUploader.vue';
import ResumeGenerator from '../components/ResumeGenerator.vue';
import JobMatcher from '../components/JobMatcher.vue';
import MockInterview from '../components/MockInterview.vue';

const activeMenu = ref('analysis');
const currentComponent = shallowRef(ResumeUploader);
const drawerVisible = ref(false); // 控制手機版抽屜開關

// 動態計算當前頁面標題
const pageTitle = computed(() => {
  const titles = {
    analysis: 'AI 履歷健檢',
    generator: 'AI 履歷撰寫',
    matcher: 'AI 職缺媒合',
    interview: 'AI 模擬面試'
  };
  return titles[activeMenu.value];
});

// 處理選單切換
const handleMenuSelect = (index) => {
  activeMenu.value = index;
  drawerVisible.value = false; // 切換功能後，自動收起手機版抽屜
  
  switch (index) {
    case 'analysis': currentComponent.value = ResumeUploader; break;
    case 'generator': currentComponent.value = ResumeGenerator; break;
    case 'matcher': currentComponent.value = JobMatcher; break;
    case 'interview': currentComponent.value = MockInterview; break;
  }
};
</script>

<style scoped>
/* 全局版面配置 */
.user-dashboard {
  display: flex;
  height: calc(100vh - 60px); /* 扣除頂部導覽列 */
  background-color: #f5f7fa;
  
  /* 🛑 核心修改：上下留 30px，左右根據螢幕寬度留 5% 的空白 */
  padding: 30px 5vw; 
  box-sizing: border-box; 
}
.main-container, .dashboard-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  
  /* 🛑 核心修改：加上圓角與立體浮動陰影 */
  background: #ffffff;
  border-radius: 16px; 
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); 
}
/* 側邊欄樣式 (SaaS 質感) */
.desktop-sidebar {
  background-color: #ffffff;
  border-right: 1px solid #e4e7ed;
  box-shadow: 2px 0 8px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
  z-index: 10;
}

.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #f0f2f5;
}

.logo-icon {
  font-size: 1.5rem;
  margin-right: 10px;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
}

.custom-menu {
  border-right: none;
  margin-top: 10px;
}
.custom-menu .el-menu-item {
  border-radius: 8px;
  margin: 0 10px 4px 10px;
  height: 48px;
  line-height: 48px;
}
.custom-menu .el-menu-item.is-active {
  background-color: #ecf5ff;
  color: #409eff;
  font-weight: bold;
}

/* 主容器與 Header */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dashboard-header {
  height: 60px;
  background-color: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

.menu-toggle {
  display: none; /* 預設桌面版隱藏 */
  font-size: 1.5rem;
  padding: 0 10px 0 0;
  color: #606266;
}

.page-title {
  margin: 0;
  font-size: 1.25rem;
  color: #303133;
}

.user-greeting {
  margin-left: 10px;
  font-size: 0.9rem;
  color: #606266;
}

/* 主內容區塊 */
.dashboard-main {
  padding: 24px;
  overflow-y: auto;
}

/* 動畫設定：Fade 結合微幅滑動，營造高級感 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(15px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}

/* 📱 響應式設定 (Media Queries) */
@media (max-width: 768px) {
  .desktop-sidebar {
    display: none; /* 手機版隱藏左側實體側邊欄 */
  }
  
  .menu-toggle {
    display: block; /* 手機版顯示漢堡按鈕 */
  }
  
  .dashboard-main {
    padding: 15px; /* 手機版縮小內邊距，保留更多螢幕空間 */
  }
  
  .user-greeting {
    display: none; /* 手機版隱藏文字，只留頭像 */
  }
}
</style>