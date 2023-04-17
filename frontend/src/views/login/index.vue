<template>
  <div class="view-account">
    <div class="view-account-header"></div>
    <div class="view-account-container">
      <div class="view-account-top">
        <div class="view-account-top-logo">
          <img :src="websiteConfig.loginImage" alt="" />
        </div>
        <div class="view-account-top-desc">{{ websiteConfig.loginDesc }}</div>
      </div>
      <div class="view-account-form">
        <n-form
          ref="formRef"
          label-placement="left"
          size="large"
          :model="formInline"
          :rules="rules"
        >
          <n-form-item path="name">
            <n-input v-model:value="formInline.name" placeholder="请输入用户名">
              <template #prefix>
                <n-icon size="18" color="#808695">
                  <PersonOutline />
                </n-icon>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item path="password">
            <n-input
              v-model:value="formInline.password"
              type="password"
              showPasswordOn="click"
              placeholder="请输入密码"
            >
              <template #prefix>
                <n-icon size="18" color="#808695">
                  <LockClosedOutline />
                </n-icon>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item class="default-color">
            <div class="flex justify-between">
              <div class="flex-initial">
                <n-checkbox v-model:checked="autoLogin">自动登录</n-checkbox>
              </div>
            </div>
          </n-form-item>
          <n-form-item>
            <n-button type="primary" @click="handleSubmit" size="large" :loading="loading" block>
              登录
            </n-button>
          </n-form-item>
          <n-form-item class="default-color">
            <div class="flex view-account-other">
              <div class="flex-initial" style="margin-left: auto">
                <a @click="register">注册账号</a>
              </div>
            </div>
          </n-form-item>
        </n-form>
      </div>
    </div>
  </div>
  <n-modal v-model:show="showModal" :show-icon="false" preset="dialog" title="用户注册">
    <n-form
      :model="formParams"
      :rules="formRules"
      ref="formRef"
      label-placement="left"
      :label-width="80"
      class="py-4"
    >
      <n-form-item label="姓名" path="name">
        <n-input placeholder="请输入姓名" v-model:value="formParams.name" />
      </n-form-item>
      <n-form-item label="昵称" path="nick_name">
        <n-input placeholder="请输入昵称" v-model:value="formParams.nick_name" />
      </n-form-item>
      <n-form-item label="联系方式" path="phone">
        <n-input placeholder="请输入联系方式" v-model:value="formParams.phone" />
      </n-form-item>
      <n-form-item label="性别" path="sex">
        <n-radio-group v-model:value="formParams.sex" name="sex">
          <n-space>
            <n-radio value="male">男</n-radio>
            <n-radio value="female">女</n-radio>
          </n-space>
        </n-radio-group>
      </n-form-item>
      <n-form-item label="密码" path="password">
        <n-input placeholder="请输入密码" v-model:value="formParams.password" />
      </n-form-item>
    </n-form>

    <template #action>
      <n-space>
        <n-button @click="() => (showModal = false)">取消</n-button>
        <n-button type="info" @click="confirmForm">确定</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script lang="ts" setup>
  import { reactive, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useUserStore } from '@/store/modules/user';
  import { FormRules, useMessage } from 'naive-ui';
  import { ResultEnum } from '@/enums/httpEnum';
  import { PersonOutline, LockClosedOutline } from '@vicons/ionicons5';
  import { PageEnum } from '@/enums/pageEnum';
  import { websiteConfig } from '@/config/website.config';
  import { userRegister } from '@/api/user/user';
  interface FormState {
    name: string;
    password: string;
  }

  const formRef = ref();
  const message = useMessage();
  const loading = ref(false);
  const autoLogin = ref(true);
  const showModal = ref(false);
  const LOGIN_NAME = PageEnum.BASE_LOGIN_NAME;

  const formInline = reactive({
    name: '',
    password: '',
    isCaptcha: true,
  });

  const rules = {
    name: { required: true, message: '请输入用户名', trigger: 'blur' },
    password: { required: true, message: '请输入密码', trigger: 'blur' },
  };

  const userStore = useUserStore();
  const router = useRouter();
  const route = useRoute();
  const formParams = reactive({
    name: '',
    nick_name: '',
    phone: '',
    password: '',
    sex: '',
  });
  // form
  const formRules: FormRules = {
    phone: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入股票代码',
      },
      {
        validator: (rule, value) => {
          const regex = /^[1][3-9][0-9]{9}$/;
          if (regex.test(value)) {
            return Promise.resolve();
          }
          return Promise.reject(new Error('请输入正确的手机号码'));
        },
        trigger: ['blur', 'input'],
      },
    ],
    name: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入姓名',
      },
    ],
    nick_name: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入昵称',
      },
    ],
    password: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入密码',
      },
    ],
    sex: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请选择性别',
      },
    ],
  };

  // 登录的方法
  const handleSubmit = (e) => {
    e.preventDefault();
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const { name, password } = formInline;
        message.loading('登录中...');
        loading.value = true;

        const params: FormState = {
          name,
          password,
        };

        try {
          const { code, message: msg } = await userStore.login(params);
          message.destroyAll();
          if (code == ResultEnum.SUCCESS) {
            const toPath = decodeURIComponent((route.query?.redirect || '/') as string);
            message.success('登录成功，即将进入系统');
            if (route.name === LOGIN_NAME) {
              router.replace('/');
            } else router.replace(toPath);
          } else {
            message.info(msg || '登录失败');
          }
        } finally {
          loading.value = false;
        }
      } else {
        message.error('请填写完整信息，并且进行验证码校验');
      }
    });
  };

  function register() {
    showModal.value = true;
    // router.push({ name: 'Register' });
  }
  function confirmForm(e) {
    e.preventDefault();
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const data = await userRegister(formParams);
        if (data.code == ResultEnum.SUCCESS) {
          window['$message'].info('用户注册成功');
        } else {
          window['$message'].error('用户注册失败, 请检查操作');
        }
        // 关闭弹窗
        setTimeout(() => {
          showModal.value = false;
        });
      } else {
        window['$message'].error('用户注册失败, 请检查操作');
      }
    });
  }
</script>

<style lang="less" scoped>
  .view-account {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: auto;

    &-container {
      flex: 1;
      padding: 32px 12px;
      max-width: 384px;
      min-width: 320px;
      margin: 0 auto;
    }

    &-top {
      padding: 32px 0;
      text-align: center;

      &-desc {
        font-size: 14px;
        color: #808695;
      }
    }

    &-other {
      width: 100%;
    }

    .default-color {
      color: #515a6e;

      .ant-checkbox-wrapper {
        color: #515a6e;
      }
    }
  }

  @media (min-width: 768px) {
    .view-account {
      background-image: url('../../assets/images/login.svg');
      background-repeat: no-repeat;
      background-position: 50%;
      background-size: 100%;
    }

    .page-account-container {
      padding: 32px 0 24px 0;
    }
  }
</style>
