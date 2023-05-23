<template>
  <div class="Home">
    <!-- =========== 最上面 ============== -->
    <div
      class="Top-welcome"
      style="display: flex; justify-content: space-between"
    >
      <!-- 左上角图+文字的盒子 -->
      <div
        class="left-top"
        style="
          display: flex;
          flex-direction: column;
          float: left;
          padding-top: 1%;
        "
      >
        <!-- 字 -->
        <div class="searchWord">
          <h1 width="40%" style="">欢迎使用图像检索系统！</h1>
        </div>
        <!-- 图 -->
        <div
          class="searchimg"
          style="display: flex; justify-content: center; align-items: center"
        >
          <img
            src="@/assets/search.png"
            alt="404"
            width="70%"
            height="100%"
            style="float: left"
          />
        </div>
      </div>

      <!-- 上传图片的框 -->
      <!-- @click绑定searchRes方法用于上传 -->
      <div class="Top-upload" style="margin-top: 5%">
        <div style="margin-bottom: 5%">
          <span>请在此处上传图片</span>
        </div>
        <UploadImage
          v-bind:fileList="fileList"
          ref="uploadImage"
          @uploadSuccess="uploadSuccess"
        />
        <el-button
          :icon="isSearching ? 'el-icon-loading' : 'el-icon-search'"
          :disabled="fileList.length == 0 || isSearching"
          @click="searchRes"
          type="primary"
          style="margin-top: 10%; z-index: 1000"
          round
        >
          点击搜索
        </el-button>
      </div>

      <div style="background: #f3e7e7; width: 0.6px; margin-right: 0%; margin-left:1%;"></div>

      <!-- 右上角 -->
      <div class="Top-collection" style="margin-top: 2%">
        <!-- 假头像 -->
        <div style="display: flex">
          <img src="../assets/avatar.png" width="40%" height="60%" />
          <div
            style="
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
            "
          >
            <span style="margin-bottom: 10%"
              >&nbsp; &nbsp; &nbsp; &nbsp; 昵称：用户1234</span
            >
            <span>身份：游客</span>
          </div>
        </div>
        <!-- 收藏按钮 点击触发函数：openCollection -->
        <div
          style="display: flex; justify-content: center; align-items: center"
        >
          <el-button
            type="primary"
            icon="el-icon-star-off"
            style="border-radius: 20px; margin-top: 6%"
            @click="openCollection"
            @changeCollect="getCollection"
            :disabled="collectDialogVisible"
            round
            >点击查看我的收藏</el-button
          >
        </div>
      </div>
    </div>

    <!-- 分割线 -->
    <el-divider></el-divider>
    <!-- 分割线 -->

    <!-- ========================== 下面 ======================= -->
    <!-- 如果没有返回图片 就404 -->
    <BlankPage v-if="responseImage.length == 0" style="z-index: 100" />

    <!-- 显示标签与图片 -->
    <div v-else>
      <div
        style="text-align: left; width: 80%; margin-left: 1%; margin-bottom: 1%"
      >
        <span style="font-weight: bold; font-size: 20px"
          >在这里可以勾选您想保留的标签！</span
        >
      </div>
      <el-col>
        <!-- tag列表 -->
        <el-row :span="5">
          <div class="label-list">
            <div v-for="(item, index) in tags" :key="index">
              <el-tag :type="labelColor[index % labelColor.length]" :hit="true">
                <el-checkbox v-model="item.status" @change="tagChange" />
                {{ item.label }}({{ item.size }})
              </el-tag>
            </div>
          </div>
        </el-row>

        <!-- 图片与tag的分割线 -->
        <div style="margin-bottom: 2%; margin-top: 2%">
          <el-divider border-color="#dcdcdc" border-style="dashed">
            <span style="font-size: 30px"
              >搜 &nbsp; 索 &nbsp; 结 &nbsp; 果</span
            >
          </el-divider>
        </div>

        <!-- 此处展示图片 -->
        <el-row :span="20">
          <div style="width: 90%; margin: 0 auto" class="containerFlex">
            <div v-for="(item, index) in responseImage" :key="index">
              <ImageCard
                :imageUrl="item"
                :disallowedTags="disallowedTags"
                :hideTags="true"
                :imageId="item"
                ref="imageCard"
              />
            </div>
          </div>
        </el-row>
      </el-col>
    </div>

    <!--收藏界面-->
    <el-dialog
      title="收藏夹"
      :visible.sync="collectDialogVisible"
      :close-on-click-modal="false"
      :modal-append-to-body="false"
      width="70%"
    >
      <div v-loading="isCollectionLoading">
        <div
          style="margin: 0 auto"
          class="containerFlex"
          v-if="collectImage.length != 0"
        >
          <div
            v-for="(item, index) in collectImage.slice(
              (currentPage - 1) * 6,
              currentPage * 6
            )"
            :key="index"
          >
            <ImageCard
              :imageUrl="item"
              :disallowedTags="disallowedTags"
              :hideTags="false"
              :imageId="item"
            />
          </div>
          <!--分页符-->
        </div>
        <div
          v-else
          style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          "
        >
          <img src="@/assets/no_collect.png" width="30%" />
          <span style="font-weight: bold; font-size: 20px; margin-bottom: 2%"
            >您暂时还没有收藏喔！</span
          >
        </div>
      </div>
      <el-pagination
        background
        layout="prev, pager, next"
        :hide-on-single-page="true"
        :page-size="3"
        @current-change="handleCurrentChange"
        :total="collectImage.length"
      >
      </el-pagination>
    </el-dialog>
  </div>
</template>

<script>
import UploadImage from "@/components/UploadImage.vue"; //引入各个子组件
import ImageCard from "@/components/ImageCard.vue";
import BlankPage from "@/components/BlankPage.vue";
import axios from "axios"; //前后端交互

export default {
  name: "Home",
  components: {
    UploadImage,
    ImageCard,
    BlankPage,
  },
  data() {
    return {
      labelColor: ["", "success", "info", "warning", "danger"],
      fileList: [],
      responseImage: [],
      filterImage: [],
      tags: [],
      disallowedTags: [],
      collectImage: [],
      collectDialogVisible: false, //确认是否弹窗：上传图片才能弹
      currentPage: 1,
      isSearching: false,
      isCollectionLoading: false,
    };
  },
  created() {
    axios({
      method: "get",
      url: "http://localhost:8080/tags",
    })
      .then((response) => {
        this.tags = response.data.map((item) => {
          item.status = true;
          return item;
        });
        this.disallowedTags = [];
      })
      .catch(() => {});
  },

  watch:{
    responseImage(newVal,oldVal){
      console.log("Home:newres,oldres",newVal,oldVal)
    }
  },

  methods: {
    uploadSuccess(response) {
      //上传图片到responseImage
      this.responseImage = response;
      this.isSearching = false;
    },

    searchRes() {
      //搜索
      this.isSearching = true;
      this.$refs.uploadImage.submitUpload(); //调用uploadimage组件的submitupload方法，提交表单
      //进一步调用el-upload的submit，进一步接入后端imgUpload接口
     
    },
    tagChange() {
      let disallowedTags = [];
      this.tags.forEach((item) => {
        if (!item.status) {
          disallowedTags.push(item.label);
        }
      });
      this.disallowedTags = disallowedTags;
    },
    openCollection() {
      this.getCollection();
      this.collectDialogVisible = true;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    getCollection() {
      this.isCollectionLoading = true;
      axios({
        method: "get",
        url: "http://localhost:8080/collect/all",
      })
        .then((response) => {
          this.collectImage = response.data;
        })
        .catch(() => {})
        .finally(() => {
          this.isCollectionLoading = false;
        });
    },
  },
};
</script>

<style scoped>
.containerFlex {
  display: flex;
  flex-direction: row;
  /*容器内成员的排列方式为从左到右*/
  flex-wrap: wrap;
  /*换行方式，放不下就换行*/
  justify-content: flex-start;
  /*项目在主轴上的对齐方式*/
  align-content: flex-start;
}

.el-divider--vertical {
  height: 60em !important;
  width: 1.5px !important;
}
.el-tag {
  float: left;
  white-space: pre-line;
  word-break: break-all;
  margin-top: 5px;
  margin-left: 5px;
}
</style>