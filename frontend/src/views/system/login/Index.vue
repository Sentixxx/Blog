<template>
    <div id="loginview">
        <el-card class="box-card">
            <h2>登录</h2>
            <el-form
                :model="ruleForm"
                status-icon
                :rules="rules"
                ref="ruleForm"
                label-position="left"
                label-width="70px"
                class="login-from"
            >
                <el-form-item label="用户名" prop="uname">
                    <el-input v-model="ruleForm.uname"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input
                        type="password"
                        v-model="ruleForm.password"
                        autocomplete="off"
                    ></el-input>
                </el-form-item>
            </el-form>
            <div class="btnGroup">
                <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
                <router-link to="/register">
                    <el-button style="margin-left: 10px">注册</el-button>
                </router-link>
            </div>
        </el-card>
    </div>
</template>

<script>
import request from '@/api/axios';
import { ElMessage } from 'element-plus';
export default {
    name: 'LoginView',
    data() {
        return {
            ruleForm: {
                uname: '',
                password: ''
            },
            rules: {
                uname: [
                    {
                        required: true,
                        message: 'UserName cannot be empty!',
                        trigger: 'blur'
                    }
                ],
                password: [
                    {
                        required: true,
                        message: 'Password cannot be empty!',
                        trigger: 'blur'
                    }
                ]
            }
        };
    },
    methods: {
        submitForm(formName) {
            return new Promise((resolve, reject) => {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        resolve();
                    } else {
                        ElMessage({
                            message: '请填写完整信息',
                            type: 'error'
                        });
                        reject();
                    }
                });
            }).then(() => {
                request
                    .post('/login', {
                        username: this.ruleForm.uname,
                        password: this.ruleForm.password
                    })
                    .then((res) => {
                        console.log(res);
                        if (res.status === 200) {
                            this.$router.push('/home');
                        }
                    })
                    .catch((error) => {
                        ElMessage({
                            message: '用户名或密码错误',
                            type: 'error'
                        });
                        console.log(error);
                    });
            });
        }
    }
};
</script>

<style scoped>
#loginview {
    display: flex;
    align-items: center; /* 在垂直方向上居中对齐 */
    justify-content: center; /* 在水平方向上居中对齐 */
    height: 100vh; /* 使元素的高度全屏 */
    overflow: hidden; /* 隐藏溢出的内容 */
}
.box-card {
    margin: auto auto;
    text-align: center;
    width: 400px;
    border-style: solid;
    border-width: 2px;
    /* border-color: #409eff; */
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
}
.login-from {
    margin: auto auto;
}
</style>
