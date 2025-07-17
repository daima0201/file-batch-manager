<template>
  <div>
    <button @click="startScan" :disabled="scanning">开始扫描</button>
    <p v-if="scanning">正在扫描，请稍候...</p>
    <ul>
      <li v-for="item in files" :key="item.id">
        {{ item.path }} - {{ item.is_file ? '文件' : '目录' }} - {{ item.size }}B
      </li>
    </ul>
  </div>
</template>

<script>
import { triggerScan, fetchScanStatus, fetchScanResults } from "@/services/api";

export default {
  data() {
    return {
      scanning: false,
      files: []
    };
  },
  methods: {
    async startScan() {
      this.scanning = true;
      await triggerScan();
      this.pollStatus();
    },
    async pollStatus() {
      const timer = setInterval(async () => {
        const { data } = await fetchScanStatus();
        if (!data.running) {
          clearInterval(timer);
          this.scanning = false;
          this.loadResults();
        }
      }, 2000);
    },
    async loadResults() {
      const { data } = await fetchScanResults();
      this.files = data;
    }
  },
  mounted() {
    this.loadResults();
  }
};
</script>