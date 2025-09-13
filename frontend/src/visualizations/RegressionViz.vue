<template>
  <el-card>
    <h3>回归任务可视化</h3>
    <div ref="scatterChart" style="width: 600px; height: 400px;"></div>
    <div ref="residualChart" style="width: 600px; height: 300px; margin-top: 20px;"></div>
  </el-card>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: {
    metrics: Object,
  },
  mounted() {
    this.drawScatter();
    this.drawResiduals();
  },
  methods: {
    drawScatter() {
      if (!this.metrics.scatter?.value) return;
      const chart = echarts.init(this.$refs.scatterChart);
      chart.setOption({
        title: { text: "预测 vs 实际" },
        xAxis: { name: "真实值" },
        yAxis: { name: "预测值" },
        series: [
          {
            type: "scatter",
            data: this.metrics.scatter.value,
            symbolSize: 3,
          },
        ],
        tooltip: { trigger: "item" },
      });
    },
    drawResiduals() {
      if (!this.metrics.residuals?.value) return;
      const residuals = this.metrics.residuals.value;

      // 🔹 手动分桶
      const binCount = 20;
      const minVal = Math.min(...residuals);
      const maxVal = Math.max(...residuals);
      const binSize = (maxVal - minVal) / binCount;

      const bins = new Array(binCount).fill(0);
      residuals.forEach((r) => {
        let idx = Math.floor((r - minVal) / binSize);
        if (idx >= binCount) idx = binCount - 1; // 防止溢出
        bins[idx]++;
      });

      const labels = Array.from({ length: binCount }, (_, i) => {
        const start = (minVal + i * binSize).toFixed(2);
        const end = (minVal + (i + 1) * binSize).toFixed(2);
        return `${start}~${end}`;
      });

      const chart = echarts.init(this.$refs.residualChart);
      chart.setOption({
        title: { text: "残差分布" },
        xAxis: { type: "category", data: labels, name: "残差区间" },
        yAxis: { type: "value", name: "频数" },
        series: [
          {
            type: "bar",
            data: bins,
          },
        ],
        tooltip: { trigger: "item" },
      });
    },
  },
};
</script>
