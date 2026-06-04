import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import UserDashboardView from '../views/UserDashboardView.vue';
// 引入 Pinia store 以便警衛查詢登入狀態
import { useAuthStore } from '../stores/auth'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    
    // 🛡️ 幫需要保護的後台路由加上 meta 標籤
    { 
      path: '/dashboard/user', 
      name: 'user-dashboard', 
      component: UserDashboardView,
      meta: { requiresAuth: true, role: 'user' } // 標記為需要登入，且身分為 user
    }, 
    { 
      path: '/dashboard/company', 
      name: 'company-dashboard', 
      component: () => import('../views/CompanyView.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    { 
      path: '/dashboard/admin', 
      name: 'admin-dashboard', 
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
  ]
});

// 🛡️ 新增：全域路由守衛 (Navigation Guard)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  // 1. 檢查這個頁面是否需要登入 (看有沒有 requiresAuth 標籤)
  if (to.meta.requiresAuth) {
    
    // 如果沒有登入，無情踢回登入頁
    if (!authStore.isLogin) {
      alert('請先登入帳號！');
      return next('/login');
    }
    
    // (進階保護) 如果登入了，但身分不符，踢回首頁
    // 例如：求職者 (user) 想硬闖管理員 (admin) 後台
    if (to.meta.role && to.meta.role !== authStore.role) {
      alert('您沒有權限訪問此頁面！');
      return next('/');
    }
  }
  
  // 檢查都通過，放行！
  next();
});

export default router;