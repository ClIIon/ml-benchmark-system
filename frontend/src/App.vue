<template>
  <div id="app">
    <h1>机器学习模型评估系统</h1>
    <BenchmarkControls @run="handleRun" />

    <div v-if="loading" class="progress">
      <el-progress :percentage="progressPercent" :text-inside="true" indeterminate />
      <p>{{ progressStatus }}</p>
    </div>


    <BenchmarkResults v-if="results" :metrics="results.metrics" :task="results.task" />
    
    <DynamicMetricsChart
      v-if="results && results.task !== 'dim_reduction' && Object.keys(metricsStore).length > 0"
      :task="results.task"
      :metricsStore="metricsStore"
    />


    <component
      v-if="results"
      :is="getVizComponent(results.task)"
      :metrics="results.metrics"
    />


  </div>
</template>

<script>
import BenchmarkControls from "./components/BenchmarkControls.vue";
import BenchmarkResults from "./components/BenchmarkResults.vue";
import ClassificationViz from "./visualizations/ClassificationViz.vue";
import RegressionViz from "./visualizations/RegressionViz.vue";
import ClusteringViz from "./visualizations/ClusteringViz.vue";
import DimReductionViz from "./visualizations/DimReductionViz.vue";
import DynamicMetricsChart from "./visualizations/DynamicMetricsChart.vue";

import { runBenchmark } from "./services/socket";

export default {
  components: {
    BenchmarkControls,
    BenchmarkResults,
    ClassificationViz,
    RegressionViz,
    ClusteringViz,
    DimReductionViz,
    DynamicMetricsChart,
  },
  data() {
    return {
      loading: false,
      progressStatus: "",
      progressPercent: 0,
      results: null,
      metricsStore: {},     
      currentDataset: null,
      currentTask: null,

    };
  },
  methods: {
    handleRun(params) {
      this.loading = true;
      this.progressStatus = "正在运行...";
      this.progressPercent = 0;
      this.results = null;

      runBenchmark(
        params,
        (progress) => {
          this.progressStatus = progress.status;
          this.progressPercent = progress.percent || this.progressPercent;
        },
        (result) => {

          this.loading = false;
          // ✅ 切换数据集/任务时清空
          if (this.currentDataset !== result.dataset || this.currentTask !== result.task) {
            this.metricsStore = {};
            this.currentDataset = result.dataset;
            this.currentTask = result.task;
          }

          // ✅ 提取数值指标
          const cleanMetrics = {};
          for (const [k, v] of Object.entries(result.metrics)) {
            if (["scatter", "residuals", "cm", "roc", "calinski"].includes(k)) continue;
            cleanMetrics[k] =
              typeof v === "object" && "value" in v ? v.value : v;
          }

          // ✅ 用新对象更新，保持响应式
          this.metricsStore = {
            ...this.metricsStore,
            [result.model]: cleanMetrics,
          };
          this.results = result;
        },
        (error) => {
          this.$message.error(error.error);
          this.loading = false;
        }
      );
    },
    getVizComponent(task) {
      switch (task) {
        case "classification":
          return "ClassificationViz";
        case "regression":
          return "RegressionViz";
        case "clustering":
          return "ClusteringViz";
        case "dim_reduction":
          return "DimReductionViz";
        default:
          return null;
      }
    },
  },
};
</script>

<style scoped>
.progress {
  margin: 20px 0;
}
</style>
