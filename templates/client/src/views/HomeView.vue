<template>
  <div class="home-view">
    <LeftPanelComponent class="left-panel" />
    <div class="home-section p-3">
      <h1 class="fs-2">Главная</h1>
      <hr>
      <h2 class="fs-3">Home</h2>
      <div class="d-flex flex-wrap">
        <div v-for="index in 4" :key="index" class="m-2 card cursor-pointer">
          <div class="card-body">
            <h4 class="card-title">Card title</h4>
            <div class="card-text">Card text</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LeftPanelComponent from '../components/LeftPanelComponent.vue';
</script>

<style scoped>
.home-view {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: stretch;
  justify-content: flex-start;
  overflow: hidden;
}

.home-section {
  flex-grow: 1;
  height: 100%;
  min-width: 0;
  overflow: hidden;
}

.left-panel {
  min-width: 60px;
  height: 100%;
  flex-shrink: 0;
}
</style>
