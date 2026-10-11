<template>
  <div style="width: 50%;margin: 5px auto">
    <div class="card" style="margin-bottom: 100px">
      <div style="font-weight: bold;font-size: 24px;margin-bottom: 50px">发表新博客/编辑博客</div>
      <el-form :model="form" label-width="100px" style="padding-right: 50px" :rules="rules" ref="formRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="标题"></el-input>
        </el-form-item>
        <el-form-item label="简介" prop="descr">
          <el-input type="textarea" v-model="form.descr" placeholder="简介"></el-input>
        </el-form-item>
        <el-form-item label="封面" prop="cover">
          <el-upload
              :action="$baseUrl + '/files/upload'"
              :headers="{ token: user.token }"
              list-type="picture"
              :on-success="handleCoverSuccess"
          >
            <el-button type="primary">上传封面</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="分类" prop="categoryId">
          <el-select v-model="form.categoryId" style="width: 100%">
            <el-option v-for="item in categoryList" :key="item.id" :value="item.id" :label="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-select v-model="tagsArr" multiple filterable allow-create default-first-option style="width: 100%">
            <el-option value="后端"></el-option>
            <el-option value="Java"></el-option>
            <el-option value="面试"></el-option>
            <el-option value="Vue"></el-option>
            <el-option value="前端"></el-option>
            <el-option value="大数据"></el-option>
            <el-option value="算法"></el-option>
            <el-option value="程序员"></el-option>
            <el-option value="小白"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <div id="editor"></div>
        </el-form-item>
      </el-form>
      <div style="text-align: center"><el-button type="primary" style="width: 100px" @click="save">发 表</el-button></div>
    </div>
  </div>
</template>

<script>
import E from "wangeditor";
import hljs from "highlight.js";

export default {
  name: "NewBlog",
  data(){
    return{
      form: {},
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      rules: {},
      tagsArr:[],
      categoryList:[],
      editor:null,
      blogId:this.$route.query.blogId,
    }
  },
  mounted() {
    if (!this.user || !this.user.id) {   // 游客不能发表博客
      this.$message.warning('该操作需要登录，请先登录或注册')
      this.$router.push('/login')
      return
    }
    this.$request.get('/category/selectAll').then(res=>{
      this.categoryList=res.data || []
    })
    this.$request.get('/blog/selectById/'+this.blogId).then(res=>{
      this.form=res.data || {}
      if(this.form.id){
        this.tagsArr=JSON.parse(this.form.tags||'[]')
        setTimeout(()=>{
          this.editor.txt.html(this.form.content)
        },0)
      }
    })

    this.setRichText()
  },
  methods:{
    save(){   // 保存按钮触发的逻辑  它会触发新增或者更新
      if (!this.user || !this.user.id) {   // 游客写操作前置检查
        this.$message.warning('该操作需要登录，请先登录或注册')
        this.$router.push('/login')
        return
      }
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          this.form.tags=JSON.stringify(this.tagsArr)//把json数组转化成json子字符串存到数据库
          this.form.content=this.editor.txt.html()//获取富文本编辑器中的html内容
          this.$request({
            url: this.form.id ? '/blog/update' : '/blog/add',
            method: this.form.id ? 'PUT' : 'POST',
            data: this.form
          }).then(res => {
            if (res.code === '200') {  // 表示成功保存
              this.$message.success('发表成功');
              setTimeout(() => {
                this.$router.push('/front/person');
              }, 1000); // 1秒后跳转
            } else {
              this.$message.error(res.msg)  // 弹出错误的信息
            }
          })
        }
      })
    },
    handleCoverSuccess(res){
      this.form.cover=res.data
    },
    setRichText() {   /*设置富文本的函数*/
      this.$nextTick(() => {
        this.editor = new E(`#editor`)  /*创建一个富文本*/
        this.editor.highlight = hljs  /*设置代码高亮*/
        this.editor.config.uploadImgServer = this.$baseUrl + '/files/editor/upload'  /*设置图片的上传地址*/
        this.editor.config.uploadFileName = 'file'   /*图片上传的名称*/
        this.editor.config.uploadImgHeaders = {     /*图片上传的token*/
          token: this.user.token
        }
        this.editor.config.uploadImgParams = {
          type: 'img',
        }
        this.editor.config.zIndex = 0  //解决分类标签遮挡
        this.editor.create()  // 创建
      })
    },

  }
}
</script>

<style scoped>

</style>