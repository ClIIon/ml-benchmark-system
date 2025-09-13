<template>
  <el-card>
    <h3>分类任务可视化</h3>
    <div ref="rocChart" style="width: 600px; height: 400px;"></div>
    <div ref="cmChart" style="width: 400px; height: 400px; margin-top: 20px;"></div>
  </el-card>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: {
    metrics: Object,
  },
  mounted() {
    this.drawROC();
    this.drawCM();
  },
  methods: {
    drawROC() {
      if (!this.metrics.roc?.value) return;
      const chart = echarts.init(this.$refs.rocChart);
      const series = [];

      Object.keys(this.metrics.roc.value).forEach((cls) => {
        const data = this.metrics.roc.value[cls].map(([fpr, tpr]) => [fpr, tpr]);
        series.push({
          name: `Class ${cls}`,
          type: "line",
          data,
          smooth: true,
        });
      });

      chart.setOption({
        title: { text: "ROC 曲线" },
        xAxis: { type: "value", min: 0, max: 1, name: "FPR" },
        yAxis: { type: "value", min: 0, max: 1, name: "TPR" },
        series,
        tooltip: { trigger: "axis" },
        legend: { top: "bottom" },
      });
    },
    drawCM() {
      if (!this.metrics.cm?.value) return;
      const chart = echarts.init(this.$refs.cmChart);
      const cm = this.metrics.cm.value;
      const size = cm.length;

      // 🔹 构造热力图数据
      const data = [];
      for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
          data.push([j, i, cm[i][j]]); // (x=预测, y=真实)
        }
      }

chart.setOption({
  title: { text: "混淆矩阵" },
  tooltip: { position: "top" },
  grid: { height: "70%", top: "10%", bottom: "10%", right: "20%" }, // ✅ 给右边预留更多空间
  xAxis: {
    type: "category",
    data: Array.from({ length: size }, (_, i) => `Pred ${i}`),
    name: "预测类别",
    nameLocation: "middle",
    nameGap: 30,
  },
  yAxis: {
    type: "category",
    data: Array.from({ length: size }, (_, i) => `True ${i}`),
    name: "真实类别",
    nameLocation: "middle",
    nameGap: 40,
  },
  visualMap: {
    min: 0,
    max: Math.max(...cm.flat()),
    calculable: true,
    orient: "vertical",
    right: "0%",
    top: "center",
    inRange: {
      color: ["#dbe9f6", "#91bfdb", "#4575b4", "#313695"]
    },
  },
  series: [
    {
      name: "Confusion Matrix",
      type: "heatmap",
      data,
      label: {
        show: true,
        formatter: (params) => (params.value[2] > 0 ? params.value[2] : ""),
        color: "#000",
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: "rgba(0, 0, 0, 0.5)",
        },
      },
    },
  ],
});



    },
  },
};
</script>
