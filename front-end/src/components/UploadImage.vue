<template>
    <div>
        <!-- 上传图片 action:执行动作的后台接口,接口是imgUpload,必须要详细给出 -->
        <!--         limit:最大上传数量 file-list:绑定文件列表 on-success:上传成功钩子 --> 
        <!--         list-type:文件列表形式  on-change:文件状态改变钩子，如添加、上传成功/失败  -->
        <el-upload 
        action="http://localhost:8080/imgUpload" 
        method="post"  
        :limit="1"
        list-type="picture-card" 
        :auto-upload="false"
        :multiple="false" 
        :file-list="fileList"
        :on-success="uploadSuccess"
        :on-change="handleChange"
        accept="image/png, image/jpeg"
        ref="uploadRef"
        :class="fileList.length >=1 ? 'styleB' : 'styleA'"
        >
            <em slot="default" class="el-icon-plus"></em>  
            
            <!-- 显示选取的图片 -->
            <div slot="file" slot-scope="{file}">
                <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                <span class="el-upload-list__item-actions">
                    <!-- 用于放大图片的icon -->
                    <span class="el-upload-list__item-preview" @click="zoom(file)">
                        <el-icon class="el-icon-zoom-in"></el-icon>
                    </span>
                    <!-- 用于删除图片的icon -->
                    <span v-if="!disabled" class="el-upload-list__item-delete" @click="removePicture(file)">
                        <el-icon class="el-icon-delete"> </el-icon>
                    </span>
                </span>
            </div>

        </el-upload>

        <!-- 弹窗，用来展示大图用 sync即把弹窗和该变量同步起来 关闭弹窗变量变false-->
        <el-dialog :visible.sync="dialogVisible">  
            <img width="80%" height="80%" :src="dialogImageUrl" alt="">
        </el-dialog>
    </div>
</template>

<script>
    export default {
        data() {
            return {  //弹窗图片
                dialogImageUrl: '',
                dialogVisible: false,
                disabled: false,
            };
        },
        props:{  //提供自身要被父组件调用的属性
            fileList: Array,
        },
        methods: {

            removePicture() {  //删除队头 即移除文件
                this.fileList.splice(0, 1);  
            },

            zoom(file) {  // 上传图片后点击放大icon，用来弹窗
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;  //控制弹窗变量
            },

            uploadSuccess(response) {  //成功上传触发 返回的response送给父组件
                this.$emit('uploadSuccess', response);  //$emit用于向父组件传值 前者为父组件调用函数 
            },

            handleChange(file){
                if (this.fileList.length >= 1) {
                    return;
                }
                this.fileList.push(file);
            },

            submitUpload(){  //提交上传
                console.log("提交上传")
                this.$refs.uploadRef.submit();  //调用el-upload的submit方法
            },
        }
    }
</script>

<style scoped>

/deep/.styleA .el-upload--picture-card{
    /* width:110px;
    height:110px;
    line-height:110px; */
    
}
/deep/.styleB .el-upload--picture-card{
    display:none;   
}

</style>