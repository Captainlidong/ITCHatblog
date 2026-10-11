<template>
  <div class="container">
    <div class="login-card" style="width: 380px; padding: 45px;">
      <div style="text-align: center; font-size: 24px; margin-bottom: 30px; color: #6b5b95">IT 论坛博客系统</div>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input size="medium" prefix-icon="el-icon-user" placeholder="请输入账号" v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input size="medium" prefix-icon="el-icon-lock" placeholder="请输入密码" show-password  v-model="form.password"></el-input>
        </el-form-item>

        <el-form-item prop="role">
          请选择登录角色：
          <el-radio-group v-model="form.role">
            <el-radio label="ADMIN">管理员</el-radio>
            <el-radio label="USER">用户</el-radio>
          </el-radio-group>
        </el-form-item>

         <!--验证码-->
        <el-form-item prop="code">
          <div style="display: flex">
            <el-input style="flex: 1" size="medium" v-model="code"></el-input>
            <Identify :identifyCode="identifyCode" @click.native="refreshCode" />
          </div>
        </el-form-item>

        <el-form-item>
          <el-button size="medium" style="width: 100%; background-color: #2a60c9; border-color: #2a60c9; color: white" @click="login">登 录</el-button>
        </el-form-item>
        <div style="display: flex; align-items: center">
          <div style="flex: 1"></div>
          <div style="flex: 1; text-align: right">
            还没有账号？请 <a href="/register">注册</a>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import Identify from "@/components/Identify.vue";

export default {
  name: "Login",
  components:{
    Identify
  },
  data() {
    return {
      form: { role: 'ADMIN' },
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
        ]
      },
      code: '',   // 表单绑定的验证码
      // 图片验证码
      identifyCode: '',
      // 验证码规则
      identifyCodes: '123456789ABCDEFGHGKMNPQRSTUVWXY',
    }
  },
  mounted() {
    this.refreshCode()
  },
  methods: {
    // 切换验证码
    refreshCode() {
      this.identifyCode = ''
      this.makeCode(this.identifyCodes, 4)
    },
    // 生成随机验证码
    makeCode(o, l) {
      for (let i = 0; i < l; i++) {
        this.identifyCode += this.identifyCodes[Math.floor(Math.random() * (this.identifyCodes.length))]
      }
    },
    login() {
      if (!this.code){
        this.$message.warning('请输入验证码！')
        this.refreshCode()
        return
      }
      if (this.code.toLowerCase()!==this.identifyCode.toLowerCase()){
        this.$message.warning('输入验证码错误！请重新输入！')
        this.refreshCode()
        return
      }
      this.$refs['formRef'].validate((valid) => {
        if (valid) {
          // 验证通过
          this.$request.post('/login', this.form).then(res => {
            if (res.code === '200') {
              localStorage.setItem("xm-user", JSON.stringify(res.data))  // 存储用户数据

              this.$message.success('登录成功')
              setTimeout(() =>{
                if (res.data.role === 'ADMIN'){
                  location.href='/home'  // 跳转主页---管理员
                }else {
                  location.href='/front/home'  // 跳转主页---用户
                }
              },500)

            } else {
              /*密码错了，验证码要刷新*/
              this.refreshCode()
              this.$message.error(res.msg)
            }
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(160deg, #c9b8f9 0%, #e3c7f7 22%, #ffd7ee 48%, #ffeaf5 66%, #c8f3e2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}
.login-card {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 22px;
  border: 1.5px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 14px 40px rgba(160, 120, 220, 0.25);
}
.login-card :deep(.el-button--medium) {
  background: linear-gradient(135deg, #b79cff, #ff9ecf) !important;
  border: none !important;
  border-radius: 999px !important;
  font-weight: bold;
  box-shadow: 0 6px 16px rgba(255, 158, 207, 0.45);
}
.login-card :deep(.el-input__inner) {
  border-radius: 999px !important;
}
a {
  color: #e8619c;
}
</style>