<template>
  <el-card>
    <el-form :inline="true" label-width="100px">
      <!-- 第一行：数据集 + 模型 -->
      <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;">
        <el-form-item label="选择数据集喵">
          <el-select v-model="dataset" placeholder="请选择数据集喵" style="width: 200px;">
            <el-option label="乳腺癌(二分类)" value="breast_cancer" />
            <el-option label="葡萄酒(多分类)" value="wine" />
            <el-option label="加州房价(回归)" value="boston" />
            <el-option label="Fashion-MNIST(图像多分类、聚类、降维)" value="fashion_mnist" />
          </el-select>
        </el-form-item>

        <el-form-item label="选择模型喵">
          <el-select v-model="model" placeholder="别忘了选择模型喵" style="width: 220px;">
            <el-option
              v-for="m in getModels(dataset)"
              :key="m"
              :label="m"
              :value="m"
            />
          </el-select>
        </el-form-item>
      </div>

      <!-- 第二行：随机种子 + 样本量 (仅在 fashion_mnist 时显示) + 按钮 -->
      <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        <el-form-item label="随机种子">
          <el-input
            v-model="seed"
            placeholder="若无，使用默认种子"
            style="width: 200px;"
          />
        </el-form-item>

        <el-form-item v-if="dataset === 'fashion_mnist'" label="样本数量">
          <el-input-number
            v-model="sample_size"
            :min="100"
            :step="100"
            placeholder="建议1000-7000"
            style="width: 200px;"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            round
            style="background: linear-gradient(90deg, #409EFF, #66b1ff); border: none;"
            @click="run"
          >
            🚀 运行Benchmarkする.
          </el-button>
        </el-form-item>
      </div>
    </el-form>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      dataset: "",
      model: "",
      seed: "",
      sample_size: 2000,
      VALID_MODELS: {
        breast_cancer: ["logistic_regression", "decision_tree", "random_forest", "svm", "knn", "naive_bayes", "gbdt"],
        wine: ["logistic_regression", "decision_tree", "random_forest", "svm", "knn", "naive_bayes"],
        boston: ["linear_regression", "decision_tree", "random_forest", "gbdt"],
        fashion_mnist: ["logistic_regression", "svm", "knn", "kmeans", "pca"],
      },
    };
  },
  methods: {
    getModels(dataset) {
      return this.VALID_MODELS[dataset] || [];
    },
    run() {
      this.$emit("run", {
        dataset: this.dataset,
        model: this.model,
        seed: this.seed,
        sample_size: this.dataset === "fashion_mnist" ? this.sample_size : null,
      });
    },
  },
};
</script>
