<script>
export default {
  name: "FileItem.vue"
}
</script>

<template>
  <div
  :class="['file-item', {selected: isSelected}]"
  @click="handleClick"
  @dblclick="handleDoubleClick"
  >
  <font-awesome-icon :icon="fileIcon" />
  <span class="file-name">{{file.name}}</span>
  <span v-if="file.type === 'file'" class="file-size">{{formatFileSize(file.size)}}</span>
</div>
</template>

<script>
  export default {
  props: {
  file: {
  type: Object,
  required: true
},
  isSelected: {
  type: Boolean,
  default: false
}
},
  computed: {
  fileIcon() {
  return this.file.type === 'directory' ? 'folder' : 'file'
}
},
  methods: {
  handleClick() {
  this.$emit('select', this.file)
},
  handleDoubleClick() {
  this.$emit('dblclick', this.file)
},
  formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
}
}
</script>

<style scoped>
.file-item {
  padding: 8px 10px;
  border-radius: 4px;
  margin-bottom: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.file-item:hover {
  background: #f0f7ff;
}

.file-item.selected {
  background: #3498db;
  color: white;
}

.file-name {
  flex: 1;
}

.file-size {
  font-size: 0.8rem;
  color: #95a5a6;
}
</style>