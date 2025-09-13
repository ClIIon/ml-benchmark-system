<template>
  <el-card>
    <h3>模型指标对比</h3>
    <!-- 加载中时展示进度条 -->
    <el-progress
      v-if="loading"
      :percentage="50"
      indeterminate
      :stroke-width="4"
      style="margin-bottom: 10px;"
    />
    <div ref="barChart" style="width: 100%; height: 400px;"></div>
  </el-card>
</template>

<script>
import * as echarts from "echarts";
import { nextTick } from "vue";

export default {
  props: {
    task: { type: String, required: true },
    // App.vue 统一管理：{ modelName: { metricName: number, ... }, ... }
    metricsStore: { type: Object, default: () => ({}) },
  },
  data() {
    return {
      chart: null,
      loading: false,
    };
  },
  watch: {
    metricsStore: {
      handler(newStore) {
        this.renderChart(newStore);
      },
      deep: true,
      immediate: true,
    },
    task() {
      this.renderChart(this.metricsStore);
    },
  },
  methods: {
    getMetricKeys(task) {
      if (task === "classification")
        return ["accuracy", "precision", "recall", "f1", "auc"];
      if (task === "regression")
        return ["MSE", "RMSE", "MAE", "R2"];
      if (task === "clustering")
        return ["silhouette", "davies_bouldin"];
      return [];
    },
    renderChart(store) {
      this.loading = true;

      nextTick(() => {
        if (!this.$refs.barChart) return;

        if (!this.chart) {
          this.chart = echarts.init(this.$refs.barChart);
        }

        const metricKeys = this.getMetricKeys(this.task);
        const models = Object.keys(store || {});

        // ✅ 确保永远有至少一个 X 轴项 和 Legend 项
        const safeMetricKeys = metricKeys.length > 0 ? metricKeys : ["placeholder"];
        const safeModels = models.length > 0 ? models : ["占位"];

        const option = {
          tooltip: {
            trigger: "axis",
            valueFormatter: (val) =>
              typeof val === "number" ? String(val) : val,
          },
          legend: { top: "bottom", data: safeModels },
          xAxis: {
            type: "category",
            data: safeMetricKeys,
            axisLabel: { rotate: 30 },
          },
          yAxis: { type: "value", min: 0 },
          series: [],
          animationDurationUpdate: 800,
          animationEasingUpdate: "cubicOut",
        };

        if (models.length > 0 && metricKeys.length > 0) {
          option.series = models.map((m) => ({
            name: m,
            type: "bar",
            data: metricKeys.map((k) => {
              const v = store[m]?.[k];
              if (typeof v === "number") return v;
              if (typeof v === "string") return Number(v) || 0;
              return 0;
            }),
            barGap: "20%",
            animationDuration: 600,
            animationEasing: "cubicOut",
            label: {
              show: true,
              position: "top",
              formatter: (p) =>
                typeof p.value === "number" ? p.value.toFixed(2) : p.value,
            },
          }));
        } else {
          // 🟢 无数据时的占位柱
          option.series = [{
            type: "bar",
            name: "占位",
            data: [0],
          }];
        }

        this.chart.setOption(option, { notMerge: false, lazyUpdate: true });

        // ⚡ 延迟 resize，确保坐标系已注册
        setTimeout(() => {
          if (this.chart) this.chart.resize();
        }, 0);

        this.loading = false;
      });
    },
    handleResize() {
      if (this.chart) this.chart.resize();
    },
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    this.renderChart(this.metricsStore);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
  },
};
</script>
