<template>
  <el-card>
    <h3>聚类任务可视化</h3>
    <!-- 聚类指标对比 -->
    <div ref="barChart" style="width: 600px; height: 300px;"></div>

    <!-- 分簇散点图 -->
    <div ref="clusterChart" style="width: 600px; height: 400px; margin-top: 20px;"></div>
  </el-card>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: { metrics: Object },
  mounted() {
    this.drawBar();
    this.drawScatter();
  },
  methods: {
    // 聚类指标对比 (柱状图)
    drawBar() {
      if (!this.metrics) return;
      const chart = echarts.init(this.$refs.barChart);

      const keys = ["silhouette", "davies_bouldin"];
      const values = keys.map((k) => this.metrics[k]?.value ?? 0);

      chart.setOption({
        title: { text: "聚类指标对比" },
        xAxis: { type: "category", data: keys },
        yAxis: { type: "value" },
        series: [
          {
            type: "bar",
            data: values,
          },
        ],
        tooltip: {
          trigger: "item",
          formatter: (p) => `${p.name}: ${p.value.toFixed(3)}`,
        },
      });
    },

    // 聚类散点 (二维降维结果 + 簇标签)
    drawScatter() {
      if (!this.metrics.scatter?.value) return;
      const chart = echarts.init(this.$refs.clusterChart);
      const scatterData = this.metrics.scatter.value;

      // 假设 scatterData 格式: [[x, y, cluster], ...]
      const labels = [...new Set(scatterData.map((d) => d[2]))];
      const series = labels.map((label) => ({
        name: `Cluster ${label}`,
        type: "scatter",
        symbolSize: 3,
        data: scatterData.filter((d) => d[2] === label).map((d) => [d[0], d[1]]),
      }));

      chart.setOption({
        title: { text: "聚类结果散点图" },
        xAxis: {},
        yAxis: {},
        legend: { top: "bottom" },
        tooltip: {
          trigger: "item",
          formatter: (p) =>
            `Cluster: ${p.seriesName}<br/>X: ${p.value[0].toFixed(
              2
            )}, Y: ${p.value[1].toFixed(2)}`,
        },
        series,
      });
    },
  },
};
</script>
