<template>
  <el-card>
    <h3>模型评估指标</h3>
    <el-table :data="rows" border>
      <el-table-column prop="metric" label="指标" width="180" />
      <el-table-column prop="value" label="数值" />
      <el-table-column prop="explanation" label="解释" />
    </el-table>
  </el-card>
</template>

<script>
export default {
  props: {
    metrics: Object,
    task: String,
  },
  computed: {
    rows() {
      return Object.keys(this.metrics)
        // ✅ 过滤掉不需要展示在表格里的字段
        .filter((k) => !["scatter", "residuals", "cm", "roc"].includes(k))
        .map((k) => {
          const item = this.metrics[k];
          return {
            metric: k,
            value:
              typeof item === "object" && "value" in item
                ? item.value
                : item,
            explanation:
              typeof item === "object" && "explanation" in item
                ? item.explanation
                : "",
          };
        });
    },
  },
};
</script>
