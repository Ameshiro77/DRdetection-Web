<template>
  <!-- 整个header的大盒子 -->
  <div
    class="header"
    style="display: flex; width: 90%; justify-content: center"
  >
    <!-- 标题 -->
    <div class="title">
      <h1
        style="
          color: #252ce8;
          letter-spacing: 10px;
          font-size: 2.3em;
          margin-left: -5%;
        "
      >
        糖尿病视网膜病变检测系统
      </h1>
    </div>
    <!-- 自己加 -->
    <div class="no!" style="margin-left: 10%;margin-top:1% ">
      <span >
       
      </span>
    </div>
  </div>
</template>


<script>
export default {
  name: "Header",
};
</script>


<style scoped>
#title {
  margin-left: 1%;
  margin-top: 1%;
  margin-bottom: 1%;
  height: 60px;
  line-height: 3.2em;
  letter-spacing: 8px;
}

i,
input,
label {
  vertical-align: middle;
}

i {
  border: 0;
  display: block;
  cursor: pointer;
}
</style>


