<template>
  <div >
    <!-- 左图 -->
    <div style="float:left" >
      <img
        src="@/assets/nosearch.png"
        alt="404"
        width="100%" height="100%"
        style="padding-left:30%; float:left; display:inline-block;"
      />
    </div>

    <!-- 右字 -->
    <div class="bullshit">
      <div class="bullshit__oops">这里似乎空荡荡的...</div>
      <div class="bullshit__headline">点击搜索框上传图片开始图像检索吧！</div>
      <span class="bullshit__info"
        ><b>我的个人博客:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b></span
      >
      <a class="bullshit__info" href="http://ameshiro77.cn">ameshiro77.cn</a>
    </div>

  </div>
</template>

<script>
export default {
  name: "Page404",
  computed: {
    message() {
      return "你似乎不能进入这个网页...";
    },
  },
  methods: {
    seeFavorite() {
      console.log("打开我的最爱");
    },
  },
};
</script>

<style lang="scss" scoped>
.bullshit {
  position: relative;
  float: left;
  width: 30%;
  margin-left: 20%;
  padding: 120px 0;
  overflow: hidden;
  &__oops {
    font-size: 32px;
    font-weight: bold;
    line-height: 40px;
    color: #6101fa;
    opacity: 0;
    margin-bottom: 20px;
    animation-name: slideUp;
    animation-duration: 0.5s;
    animation-fill-mode: forwards;
  }
  &__headline {
    font-size: 20px;
    line-height: 24px;
    color: #222;
    font-weight: bold;
    opacity: 0;
    margin-bottom: 10px;
    animation-name: slideUp;
    animation-duration: 0.5s;
    animation-delay: 0.1s;
    animation-fill-mode: forwards;
  }
  &__info {
    font-size: 13px;
    line-height: 21px;
    color: grey;
    opacity: 0;
    margin-bottom: 30px;
    animation-name: slideUp;
    animation-duration: 0.5s;
    animation-delay: 0.2s;
    animation-fill-mode: forwards;
  }
  &__return-home {
    display: block;
    float: left;
    margin-left: 100px;
    width: 110px;
    height: 36px;
    background: #1482f0;
    border-radius: 100px;
    text-align: center;
    color: #ffffff;
    opacity: 0;
    font-size: 14px;
    line-height: 36px;
    cursor: pointer;
    animation-name: slideUp;
    animation-duration: 0.5s;
    animation-delay: 0.3s;
    animation-fill-mode: forwards;
  }
  @keyframes slideUp {
    0% {
      transform: translateY(60px);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }
}
</style>
