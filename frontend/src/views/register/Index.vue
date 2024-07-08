<template>
    <div id="registerview">
        <el-card class="box-card">
            <h2>注册</h2>
            <el-form
                :model="ruleForm"
                status-icon
                :rules="rules"
                ref="ruleForm"
                label-position="left"
                label-width="80px"
                class="demo-ruleForm"
            >
                <el-form-item label="用户名" prop="uname">
                    <el-input v-model="ruleForm.uname"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pass">
                    <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="password">
                    <el-input
                        type="password"
                        v-model="ruleForm.password"
                        autocomplete="off"
                    ></el-input>
                </el-form-item>
            </el-form>
            <div class="btnGroup">
                <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                <el-button @click="goBack">返回</el-button>
            </div>
        </el-card>
    </div>
</template>

<script>
import request from '@/api/plugins/axios';
export default {
    data() {
        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else {
                if (this.ruleForm.checkPass !== '') {
                    this.$refs.ruleForm.validateField('checkPass');
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.ruleForm.pass) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        };
        return {
            ruleForm: {
                uname: '',
                pass: '',
                password: ''
            },
            rules: {
                uname: [{ required: true, message: '用户名不能为空！', trigger: 'blur' }],
                pass: [{ required: true, validator: validatePass, trigger: 'blur' }],
                password: [{ required: true, validator: validatePass2, trigger: 'blur' }]
            }
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    alert('submit!');
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
            request
                .post('/register', {
                    username: this.ruleForm.uname,
                    password: this.ruleForm.pass
                })
                .then((res) => {
                    console.log(res);
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        goBack() {
            this.$router.go(-1);
        }
    }
};
</script>

<style scoped>
#registerview {
    display: flex;
    align-items: center; /* 在垂直方向上居中对齐 */
    justify-content: center; /* 在水平方向上居中对齐 */
    height: 100vh; /* 使元素的高度全屏 */
    overflow: hidden; /* 隐藏溢出的内容 */

    /*设置半透明*/
}
.box-card {
    margin: 0 auto;
    width: 400px;
    border-style: solid;
    /* bsorder-width: 2px; */
    /* border-color: #409eff; */
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
}
.login-from {
    margin: auto auto;
}
.btnGroup {
    margin-top: 20px;
    text-align: center;
}
</style>
