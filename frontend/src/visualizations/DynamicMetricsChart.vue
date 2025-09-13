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
    metricsStore: { type: Object, default: () => ({}) },
  },
  data() {
    return {
      chart: null,
      loading: false,
      firstRender: true, // ✅ 首次渲染标记
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

        if (models.length === 0) {
          this.chart.clear();
          this.loading = false;
          return;
        }

        const safeMetricKeys = metricKeys.length > 0 ? metricKeys : ["占位指标"];
        const safeModels = models.length > 0 ? models : ["占位模型"];

        const option = {
          animation: true,
          animationDuration: this.firstRender ? 1000 : 300, // ✅ 首次渐入更慢
          animationEasing: "cubicOut",
          animationDurationUpdate: 600,
          animationEasingUpdate: "cubicOut",

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
        };

        if (metricKeys.length > 0 && models.length > 0) {
          option.series = models.map((m) => ({
            id: m, // ✅ 稳定 ID 触发过渡动画
            name: m,
            type: "bar",
            barGap: "20%",
            animation: true,
            animationDuration: this.firstRender ? 1000 : 300,
            animationEasing: "cubicOut",
            animationDurationUpdate: 600,
            animationEasingUpdate: "cubicOut",
            data: metricKeys.map((k) => {
              const v = store[m]?.[k];
              if (typeof v === "number") return v;
              if (typeof v === "string") return Number(v) || 0;
              return 0;
            }),
            label: {
              show: true,
              position: "top",
              formatter: (p) =>
                typeof p.value === "number" ? p.value.toFixed(2) : p.value,
            },
          }));
        } else {
          option.series = [
            {
              id: "placeholder",
              name: "占位模型",
              type: "bar",
              animation: true,
              data: [0],
            },
          ];
        }

        this.chart.setOption(option, false);

        this.firstRender = false; // ✅ 渲染后取消首次标记
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
