<template>
  <el-card>
    <h3>降维任务可视化 (PCA)</h3>
    <div ref="pcaChart" style="width: 600px; height: 400px;"></div>
    <div ref="evrChart" style="width: 600px; height: 300px; margin-top: 20px;"></div>
  </el-card>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: { metrics: Object },
  mounted() {
    this.drawScatter();
    this.drawEVR();
  },
  methods: {
    drawScatter() {
      if (!this.metrics.scatter?.value) return;
      const chart = echarts.init(this.$refs.pcaChart);
      const scatterData = this.metrics.scatter.value;
      const hasLabel = scatterData[0].length === 3;

      let series = [];
      if (hasLabel) {
        const labels = [...new Set(scatterData.map((d) => d[2]))];
        series = labels.map((label) => ({
          name: `Class ${label}`,
          type: "scatter",
          symbolSize: 3,
          data: scatterData
            .filter((d) => d[2] === label)
            .map((d) => [d[0], d[1]]),
        }));
      } else {
        series = [
          {
            name: "Samples",
            type: "scatter",
            symbolSize: 3,
            data: scatterData.map((d) => [d[0], d[1]]),
          },
        ];
      }

      chart.setOption({
        title: { text: "二维 PCA 散点图" },
        xAxis: { name: "PC1" },
        yAxis: { name: "PC2" },
        legend: hasLabel ? { top: "bottom" } : null,
        tooltip: {
          trigger: "item",
          formatter: (p) =>
            hasLabel
              ? `Class: ${p.seriesName}<br/>PC1: ${p.value[0].toFixed(
                  2
                )}, PC2: ${p.value[1].toFixed(2)}`
              : `PC1: ${p.value[0].toFixed(2)}, PC2: ${p.value[1].toFixed(2)}`,
        },
        series,
      });
    },
    drawEVR() {
      if (!this.metrics["Explained Variance Ratio"]?.value) return;
      const chart = echarts.init(this.$refs.evrChart);
      chart.setOption({
        title: { text: "解释方差比例" },
        xAxis: {
          type: "category",
          data: this.metrics["Explained Variance Ratio"].value.map(
            (_, i) => `PC${i + 1}`
          ),
        },
        yAxis: { type: "value" },
        series: [
          {
            type: "bar",
            data: this.metrics["Explained Variance Ratio"].value,
          },
        ],
        tooltip: { trigger: "item" },
      });
    },
  },
};
</script>
