<!-- eslint-disable no-console -->
<template>
  <div id="Content">
    <el-dialog
      title="AI预测中"
      :visible.sync="dialogTableVisible"
      :show-close="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :center="true"
    >
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">请耐心等待约3秒钟</span>
    </el-dialog>
    <div id="CT">
      <!-- 传图片，显示图片的div 以及显示对应颜色对应图例 -->
      <div id="CT_image">
        <!-- 用card的方式显示 -->
        <el-card
          id="CT_image_1"
          class="box-card"
          style="
            border-radius: 8px;
            width: 100%;
            height: 400px;
            margin-bottom: -30px;
          "
        >
          <div style="display: flex">
            <!-- 上传的图 -->
            <div class="demo-image__preview1">
              <div
                v-loading="loading"
                element-loading-text="上传图片中"
                element-loading-spinner="el-icon-loading"
              >
                <el-image
                  :src="url_input"
                  class="image_1"
                  :preview-src-list="[url_input]"
                  style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      <el-button
                        v-show="showbutton"
                        type="primary"
                        icon="el-icon-upload"
                        class="download_bt"
                        v-on:click="true_upload"
                      >
                        上传图像
                        <input
                          ref="upload"
                          style="display: none"
                          name="file"
                          type="file"
                          @change="update"
                        />
                      </el-button>
                    </div>
                  </div>
                </el-image>
              </div>
              <div class="img_info_1" style="border-radius: 0 0 5px 5px">
                <span style="color: white; letter-spacing: 6px">原始图像</span>
              </div>
            </div>

            <!-- 结果的图 -->
            <div class="demo-image__preview2">
              <div
                v-loading="loading"
                element-loading-text="处理中,请耐心等待"
                element-loading-spinner="el-icon-loading"
              >
                <el-image
                  :src="url_result"
                  class="image_1"
                  :preview-src-list="[url_result]"
                  style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      {{ wait_return }}
                    </div>
                  </div>
                </el-image>
              </div>
              <div class="img_info_1" style="border-radius: 0 0 5px 5px">
                <span style="color: white; letter-spacing: 4px">检测结果</span>
              </div>
            </div>
            
            <!-- 结果的图 -->
            <div class="demo-image__preview2">
              <div
                v-loading="loading"
                element-loading-text="处理中,请耐心等待"
                element-loading-spinner="el-icon-loading"
              >
                <el-image
                  :src="real_label"
                  class="image_1"
                  :preview-src-list="[real_label]"
                  style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      {{ wait_return }}
                    </div>
                  </div>
                </el-image>
              </div>
              <div class="img_info_1" style="border-radius: 0 0 5px 5px">
                <span style="color: white; letter-spacing: 4px">实际结果</span>
              </div>
            </div>

            <!-- 一个简单的图例 -->

            <div class="legend" style="margin-left: 5%; margin-top: 10%">
              <div style="display: flex">
                <div
                  style="
                    background-color: rgb(128, 0, 0);
                    width: 10px;
                    height: 10px;
                  "
                ></div>
                <span>&nbsp; EX</span>
              </div>
              <div style="display: flex">
                <div
                  style="
                    background-color: rgb(0, 128, 0);
                    width: 10px;
                    height: 10px;
                  "
                ></div>
                <span>&nbsp; HE</span>
              </div>
              <div style="display: flex">
                <div
                  style="
                    background-color: rgb(128, 128, 0);
                    width: 10px;
                    height: 10px;
                  "
                ></div>
                <span>&nbsp; SE</span>
              </div>
              <div style="display: flex">
                <div
                  style="
                    background-color: rgb(0, 0, 128);
                    width: 10px;
                    height: 10px;
                  "
                ></div>
                <span>&nbsp; MA</span>
              </div>
            </div>
          </div>

          <!-- 重新选择图像按钮 -->
          <div class="reupload" style="margin-left: 12%">
            <el-button
              style="margin-left: 35px"
              v-show="!showbutton"
              type="primary"
              icon="el-icon-upload"
              class="download_bt"
              v-on:click="true_upload2"
            >
              重新选择图像
              <input
                ref="upload2"
                style="display: none"
                name="file"
                type="file"
                @change="update"
              />
            </el-button>
          </div>
        </el-card>
      </div>
      <div>
        <el-table
      :data="tableData"
      border
      style="width:100%">
      <el-table-column
        prop="type"
        label="像素类型"
        >
      </el-table-column>
      <el-table-column
        prop="iou"
        label="Iou"
        >
      </el-table-column>
      <el-table-column
        prop="recall"
        label="recall"
        >
      </el-table-column>
      <el-table-column
        prop="precision"
        label="precision"
        >
      </el-table-column>
    </el-table>

      </div>

      <div id="info_patient">
        <!-- 卡片放置表格 -->
        <el-card style="border-radius: 8px; width: 100%">
          <div slot="header" class="clearfix">
            <div style="width: 100%; text-align: left">
              <span>分类结果：</span>
              <span style="color: rgb(255, 93, 109)">{{ classify }}</span>
            </div>
          </div>

          <div slot="header" class="clearfix">
            <div style="width: 100%; text-align: left">
              <span>置信度：</span>
              <span style="color: rgb(255, 93, 109)">{{ classify_p }}</span>
            </div>
          </div>

          <div>
            <span>{{ text }}</span>
          </div>
        </el-card>
      </div>
    </div>
    
    
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Content",
  data() {
    return {
      label_url: "http://127.0.0.1:8000/static/label/", //预测结果的地址,label_url+xxx.jpg 即src
      real_url:"http://127.0.0.1:8000/static/real_label/",   //实际标签的地址
      centerDialogVisible: true,
      real_label:'',

      url_input: "", //上传图片的url
      url_result: "", //结果图片的url
      url: "", //无视 获取url用

      classify: "", //分类结果
      classify_p:"",
      text:"",//医疗建议
      wait_return: "等待上传",
      wait_upload: "等待上传",
      loading: false,
      showbutton: true,
      percentage: 0,
      dialogTableVisible: false,
      tableData: []
    };
  },

  created: function () {
    //网页名字
    document.title = "DR检测demo";
  },

  methods: {
    true_upload() {
      this.$refs.upload.click();
    },
    true_upload2() {
      this.$refs.upload2.click();
    },

    // 获得目标文件
    getObjectURL(file) {
      var url = null;
      if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
      } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },

    // 上传文件
    update(e) {
      this.percentage = 0;
      this.dialogTableVisible = true;
      this.url_input = "";
      this.url_result = "";
      this.wait_return = "";
      this.wait_upload = "";
      this.loading = true; //开启加载
      this.showbutton = false;

      let file = e.target.files[0]; //拿去文件
      this.url_input = this.$options.methods.getObjectURL(file); //url_input：上传的图片所在的地址

      let param = new FormData(); //创建form对象
      param.append("file", file, file.name); //通过append向form对象添加数据

      var timer = setInterval(() => {
        this.myFunc();
      }, 30);

      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      }; //添加请求头

      axios
        .post("http://127.0.0.1:8000/imgUpload", param, config)
        .then((response) => {
          // eslint-disable-next-line no-console
          console.log(response);
          // eslint-disable-next-line no-console
          //console.log(response.data['filename']);
          this.percentage = 100;
          clearInterval(timer);
          this.url_result = this.label_url + response.data[0]['filename'];
          this.real_label=this.real_url    + response.data[0]['filename'].replace(".jpg", ".png");
          // eslint-disable-next-line no-console
          console.log(this.real_label)
          this.classify_p = response.data[0]['probability']
          this.classify = response.data[0]['label'];
          this.text=response.data[0]['text']
          // eslint-disable-next-line no-console
          this.updateMetric(response.data[1]);

          this.dialogTableVisible = false;
          this.loading = false;

          this.percentage = 0;
          this.putNotice(); //提示预测成功
        });
    },
    //更新指标
    updateMetric(metric){
      var name=["background","EX", "HE", "SE", "MA"]
      this.tableData=[]
      for(let i=0;i<metric[0].length;i++){
        if(metric[0][i]!="0"){
          let obj={}
          obj.type=name[i]; //获取名字
          obj.iou=metric[0][i];
          obj.recall=metric[1][i];
          obj.precision=metric[2][i];
          this.tableData.push(obj);
        }
      }

    },
    myFunc() {
      if (this.percentage + 33 < 99) {
        this.percentage = this.percentage + 33;
      } else {
        this.percentage = 99;
      }
    },
    
    putNotice() {
      this.$notify({
        title: "预测成功",
        message: "点击图片可以查看大图",
        duration: 5000,
        type: "success",
      });
    },
  },

  mounted() {
    // eslint-disable-next-line no-console
    console.log("组件挂载完毕");
  },
};
</script>

<style>
.el-button {
  padding: 12px 20px !important;
}

#hello p {
  font-size: 15px !important;
  /*line-height: 25px;*/
}

.n1 .el-step__description {
  padding-right: 20%;
  font-size: 14px;
  line-height: 20px;
  /* font-weight: 400; */
}
</style>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.dialog_info {
  margin: 20px auto;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  margin-top: -20px;
}

.divider {
  width: 50%;
}

#CT {
  height: 100%;
  width: 100%;
  flex-wrap: wrap;
  justify-content: center;
  margin: 0 auto;
  margin-right: 0px;
}

#CT_image_1 {
  width: 90%;
  height: 40%;
  margin: 0px auto;
  padding: 0px auto;
  margin-right: 180px;
  margin-bottom: 0px;
  border-radius: 4px;
}

#CT_image {
  margin-bottom: 60px;
  margin-left: 30px;
  margin-top: 5px;
}

.image_1 {
  width: 275px;
  height: 260px;
  background: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #63aff5;
  line-height: 30px;
}

.demo-image__preview1 {
  width: 250px;
  height: 290px;
  margin: 20px 60px;
  float: left;
}

.demo-image__preview2 {
  width: 250px;
  height: 290px;

  margin: 20px 60px;
  /* background-color: green; */
}

.error {
  margin: 100px auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}

.block-sidebar {
  position: fixed;
  display: none;
  left: 50%;
  margin-left: 600px;
  top: 350px;
  width: 60px;
  z-index: 99;
}

.block-sidebar .block-sidebar-item {
  font-size: 50px;
  color: lightblue;
  text-align: center;
  line-height: 50px;
  margin-bottom: 20px;
  cursor: pointer;
  display: block;
}

div {
  display: block;
}

.block-sidebar .block-sidebar-item:hover {
  color: #63aff5;
}

.download_bt {
  padding: 10px 16px !important;
}

#upfile {
  width: 104px;
  height: 45px;
  background-color: #63aff5;
  color: #fff;
  text-align: center;
  line-height: 45px;
  border-radius: 3px;
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
  color: #fff;
  font-family: "Source Sans Pro", Verdana, sans-serif;
  font-size: 0.875rem;
}

.file {
  width: 200px;
  height: 130px;
  position: absolute;
  left: -20px;
  top: 0;
  z-index: 1;
  -moz-opacity: 0;
  -ms-opacity: 0;
  -webkit-opacity: 0;
  opacity: 0; /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
  filter: alpha(opacity=0);
  cursor: pointer;
}

#upload {
  position: relative;
  margin: 0px 0px;
}

#Content {
  width: 100%;
  background-color: #ffffff;
  margin: 15px auto;
}

.divider {
  background-color: #eaeaea !important;
  height: 2px !important;
  width: 100%;
  margin-bottom: 50px;
}

.divider_1 {
  background-color: #ffffff;
  height: 2px !important;
  width: 100%;
  margin-bottom: 20px;
  margin: 20px auto;
}

.steps {
  font-family: "lucida grande", "lucida sans unicode", lucida, helvetica,
    "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
  color: #63aff5;
  text-align: center;
  margin: 15px auto;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.step_1 {
  /*color: #303133 !important;*/
  margin: 20px 26px;
}

#info_patient {
  width: 100%;
  margin-top: 5px;
  justify-content: center;
  display: flex;
  
}
</style>


