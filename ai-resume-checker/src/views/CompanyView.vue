<template>
  <div class="company-dashboard">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>🏢 企業徵才控制台</h2>
        </div>
      </template>
      
      <el-empty description="目前尚未新增任何職缺 (JD)" />
      
      <div class="action-area text-center mt-4">
        <el-button type="primary" size="large">發布新職缺</el-button>
        <el-button type="success" size="large" plain>查看 AI 推薦名單</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 未來企業上傳 JD 的邏輯會寫在這裡
</script>

<style scoped>
.company-dashboard {
  max-width: 800px;
  margin: 0 auto;
}
.card-header h2 {
  margin: 0;
  color: #303133;
  text-align: center;
}
.text-center {
  text-align: center;
}
.mt-4 {
  margin-top: 1rem;
}
</style>