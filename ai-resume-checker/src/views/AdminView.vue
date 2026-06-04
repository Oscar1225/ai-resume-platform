<template>
  <div class="admin-dashboard">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>⚙️ 系統管理員後台</h2>
        </div>
      </template>

      <el-row :gutter="20" class="statistics-row">
        <el-col :span="8">
          <el-statistic title="今日活躍用戶" :value="125" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="AI 履歷分析次數" :value="89" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="待處理客服" :value="3" />
        </el-col>
      </el-row>

      <el-divider />

      <div class="action-area text-center mt-4">
        <el-button type="warning" size="large">管理使用者權限</el-button>
        <el-button type="primary" size="large" plain>回覆客服訊息</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 未來管理員的資料請求與權限控管邏輯會寫在這裡
</script>

<style scoped>
.admin-dashboard {
  max-width: 800px;
  margin: 0 auto;
}
.card-header h2 {
  margin: 0;
  color: #303133;
  text-align: center;
}
.statistics-row {
  text-align: center;
  margin: 20px 0;
}
.text-center {
  text-align: center;
}
.mt-4 {
  margin-top: 1rem;
}
</style>