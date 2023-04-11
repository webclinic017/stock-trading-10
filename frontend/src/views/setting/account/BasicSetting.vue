<template>
  <n-grid cols="2 s:2 m:2 l:3 xl:3 2xl:3" responsive="screen">
    <n-grid-item>
      <n-form :label-width="80" :model="formValue" :rules="rules" ref="formRef">
        <n-form-item label="姓名" path="name">
          <n-input v-model:value="formValue.name" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="昵称" path="nick_name">
          <n-input v-model:value="formValue.nick_name" placeholder="请输入昵称" />
        </n-form-item>
        <n-form-item label="联系电话" path="phone">
          <n-input placeholder="请输入联系电话" v-model:value="formValue.phone" />
        </n-form-item>
        <div>
          <n-space>
            <n-button type="primary" @click="formSubmit">更新基本信息</n-button>
          </n-space>
        </div>
      </n-form>
    </n-grid-item>
  </n-grid>
</template>

<script lang="ts" setup>
  import { onMounted, reactive, ref } from 'vue';
  import { useMessage } from 'naive-ui';
  import { getUserInfo, updateUserInfo } from '@/api/user/user';
  import { ResultEnum } from '@/enums/httpEnum';

  const rules = {
    name: {
      required: true,
      message: '请输入昵称',
      trigger: 'blur',
    },
    nick_name: {
      message: '请输入邮箱',
      trigger: 'blur',
    },
    phone: {
      message: '请输入联系电话',
      trigger: 'input',
    },
  };
  const formRef: any = ref(null);
  const message = useMessage();

  const formValue = reactive({
    name: '',
    nick_name: '',
    phone: '',
  });

  onMounted(async () => {
    const userInfo = await getUserInfo();
    formValue.name = userInfo.name;
    formValue.nick_name = userInfo.nick_name;
    formValue.phone = userInfo.phone;
  });

  function formSubmit() {
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const res = await updateUserInfo(formValue);
        if (res.code == ResultEnum.SUCCESS) {
          window['$message'].info('信息修改成功');
        } else {
          window['$message'].error('用户信息修改失败, 请重新输入');
        }
      } else {
        message.error('验证失败，请填写完整信息');
      }
    });
  }
</script>
