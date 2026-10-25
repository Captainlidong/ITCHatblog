<template>
  <div class="container">
    <div class="login-card" style="width: 380px; padding:50px 30px;">
      <div style="text-align: center; font-size: 24px; margin-bottom: 30px; color: #6b5b95">欢迎注册IT论坛博客账号</div>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input prefix-icon="el-icon-user" size="medium" placeholder="请输入账号" v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input prefix-icon="el-icon-lock" size="medium" placeholder="请输入密码" show-password  v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item prop="confirmPass">
          <el-input prefix-icon="el-icon-lock" size="medium"  placeholder="请确认密码" show-password  v-model="form.confirmPass"></el-input>
        </el-form-item>
        <!--验证码（服务端生成+校验）-->
        <el-form-item prop="code">
          <div style="display: flex">
            <el-input style="flex: 1" size="medium" v-model="code" placeholder="请输入验证码"></el-input>
            <img v-if="captchaImg" :src="captchaImg" @click="loadCaptcha" title="点击刷新验证码"
                 style="height: 36px; margin-left: 8px; border-radius: 6px; cursor: pointer; border: 1px solid #e9d5ff">
          </div>
        </el-form-item>
        <el-form-item>
          <el-button style="width: 100%; background-color: #2a60c9; border-color: #2a60c9; color: white" size="medium"  @click="register">注 册</el-button>
        </el-form-item>
        <div style="display: flex; align-items: center">
          <div style="flex: 1"></div>
          <div style="flex: 1; text-align: right">
            已有账号？请 <a href="/login">登录</a>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    // 验证码校验
    const validatePassword = (rule, confirmPass, callback) => {
      if (confirmPass === '') {
        callback(new Error('请确认密码'))
      } else if (confirmPass !== this.form.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      form: {role:'USER'},
      code: '',   // 表单绑定的验证码
      captchaId: '',   // 服务端签发的验证码ID
      captchaImg: '',  // 服务端生成的验证码图片（base64）
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
        ],
        confirmPass: [
          { validator: validatePassword, trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadCaptcha()
  },
  methods: {
    // 从服务端获取新验证码
    loadCaptcha() {
      this.$request.get('/captcha/generate').then(res => {
        if (res.code === '200') {
          this.captchaId = res.data.captchaId
          this.captchaImg = res.data.captchaImage
        }
      })
    },
    register() {
      if (!this.code){
        this.$message.warning('请输入验证码！')
        this.loadCaptcha()
        return
      }
      this.$refs['formRef'].validate((valid) => {
        if (valid) {
          // 验证通过
          this.$request.post('/register', { ...this.form, captchaId: this.captchaId, captchaCode: this.code }).then(res => {
            if (res.code === '200') {
              this.$router.push('/')  // 跳转登录页面
              this.$message.success('注册成功')
            } else {
              this.$message.error(res.msg)
              this.loadCaptcha()
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