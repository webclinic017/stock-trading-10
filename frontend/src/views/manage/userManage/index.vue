<template>
  <n-card :bordered="false" class="proCard">
    <BasicForm @register="register" @submit="handleSubmit" @reset="handleReset">
      <template #statusSlot="{ model, field }">
        <n-input v-model:value="model[field]" />
      </template>
    </BasicForm>
    <BasicTable
      :columns="columns"
      :request="loadDataTable"
      :row-key="(row) => row.id"
      ref="actionRef"
      :actionColumn="actionColumn"
      @edit-change="onEditChange"
      @update:checked-row-keys="onCheckedRow"
      :scroll-x="1590"
    >
      <template #tableTitle>
        <n-button type="primary" @click="add">
          <template #icon>
            <n-icon>
              <PlusOutlined />
            </n-icon>
          </template>
          新增用户
        </n-button>
      </template>
      <template #toolbar>
        <n-button type="primary" @click="reloadTable">刷新数据</n-button>
      </template>
    </BasicTable>

    <n-modal v-model:show="showModal" :show-icon="false" preset="dialog" title="新增用户">
      <n-form
        :model="formParams"
        :rules="formRules"
        ref="formRef"
        label-placement="left"
        :label-width="80"
        class="py-4"
      >
        <n-form-item label="名称" path="name">
          <n-input placeholder="请输入名称" v-model:value="formParams.name" />
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
        <n-form-item label="角色" path="role">
          <n-radio-group v-model:value="formParams.role" name="role">
            <n-space>
              <n-radio value="admin">管理员</n-radio>
              <n-radio value="user">普通用户</n-radio>
            </n-space>
          </n-radio-group>
        </n-form-item>
      </n-form>

      <template #action>
        <n-space>
          <n-button @click="() => (showModal = false)">取消</n-button>
          <n-button type="info" :loading="formBtnLoading" @click="confirmForm">确定</n-button>
        </n-space>
      </template>
    </n-modal>

    <n-modal v-model:show="showEditModal" :show-icon="false" preset="dialog" title="编辑用户">
      <n-form
        :model="editFormParams"
        ref="editFormRef"
        label-placement="left"
        :label-width="80"
        class="py-4"
      >
        <n-form-item label="名称" path="name">
          <n-input placeholder="请输入名称" v-model:value="editFormParams.name" />
        </n-form-item>
        <n-form-item label="昵称" path="nick_name">
          <n-input placeholder="请输入昵称" v-model:value="editFormParams.nick_name" />
        </n-form-item>
        <n-form-item label="联系方式" path="phone">
          <n-input placeholder="请输入联系方式" v-model:value="editFormParams.phone" />
        </n-form-item>
        <n-form-item label="性别" path="sex">
          <n-radio-group v-model:value="editFormParams.sex" name="sex">
            <n-space>
              <n-radio value="male">男</n-radio>
              <n-radio value="female">女</n-radio>
            </n-space>
          </n-radio-group>
        </n-form-item>
        <n-form-item label="角色" path="role">
          <n-radio-group v-model:value="editFormParams.role" name="role">
            <n-space>
              <n-radio value="admin">管理员</n-radio>
              <n-radio value="user">普通用户</n-radio>
            </n-space>
          </n-radio-group>
        </n-form-item>
        <n-form-item label="状态" path="status">
          <n-radio-group v-model:value="editFormParams.status" name="status">
            <n-space>
              <n-radio value="禁用">禁用</n-radio>
              <n-radio value="启用">启用</n-radio>
            </n-space>
          </n-radio-group>
        </n-form-item>
      </n-form>

      <template #action>
        <n-space>
          <n-button @click="() => (showModal = false)">取消</n-button>
          <n-button type="info" :loading="formBtnLoading" @click="handleSave">修改</n-button>
        </n-space>
      </template>
    </n-modal>
  </n-card>
</template>

<script lang="ts" setup>
  import { h, reactive, ref } from 'vue';
  import { BasicTable, TableAction } from '@/components/Table';
  import { BasicForm, FormSchema, useForm } from '@/components/Form/index';
  import { columns } from './columns';
  import { PlusOutlined } from '@vicons/antd';
  import { type FormRules } from 'naive-ui';
  import { ResultEnum } from '@/enums/httpEnum';
  import { getList, editUser, deleteUser, addUser } from '@/api/user/user';

  const formRef: any = ref(null);
  const editFormRef: any = ref(null);
  const actionRef = ref();
  const currentEditKeyRef = ref('');
  const showModal = ref(false);
  const showEditModal = ref(false);
  const formBtnLoading = ref(false);

  // form
  const formRules: FormRules = {
    name: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入名称',
    },
    phone: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入联系方式',
    },
    sex: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请选择性别',
    },
    role: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请选择角色',
    },
  };
  const formParams = reactive({
    name: '',
    nick_name: '',
    phone: '',
    sex: '',
    role: '',
  });
  const editFormParams = reactive({
    user_id: '',
    name: '',
    nick_name: '',
    phone: '',
    sex: '',
    role: '',
    status: '',
  });

  // schemas
  const schemasParams = reactive({
    name: '',
    phone: '',
    status: '',
    sex: '',
  });
  const schemas: FormSchema[] = [
    {
      field: 'name',
      component: 'NInput',
      label: '姓名',
      componentProps: {
        placeholder: '请输入姓名',
        onInput: (e: any) => {
          console.log(e);
        },
      },
      rules: [{ message: '请输入姓名', trigger: ['blur'] }],
    },
    {
      field: 'phone',
      component: 'NInputNumber',
      label: '联系方式',
      componentProps: {
        placeholder: '请输入手机号码',
        showButton: false,
        onInput: (e: any) => {
          console.log(e);
        },
      },
    },
    {
      field: 'status',
      component: 'NRadioGroup',
      label: '状态',
      componentProps: {
        options: [
          {
            label: '启用',
            value: '启用',
          },
          {
            label: '禁用',
            value: '禁用',
          },
        ],
      },
    },
    {
      field: 'sex',
      component: 'NRadioGroup',
      label: '性别',
      componentProps: {
        options: [
          {
            label: '男',
            value: 'male',
          },
          {
            label: '女',
            value: 'female',
          },
        ],
      },
    },
  ];
  const [register, {}] = useForm({
    gridProps: { cols: '1 s:1 m:2 l:3 xl:4 2xl:4' },
    labelWidth: 80,
    schemas,
  });

  // action
  const actionColumn = reactive({
    width: 150,
    title: '操作',
    key: 'action',
    fixed: 'right',
    align: 'center',
    render(record) {
      return h(TableAction, {
        style: 'button',
        actions: createActions(record),
      });
    },
  });

  // table
  const loadDataTable = async (res) => {
    const data = await getList({ ...res, ...schemasParams });
    if (data.code == ResultEnum.SUCCESS) {
      window['$message'].info('查询成功');
      return data.result;
    } else {
      window['$message'].error('没有符合条件的数据, 请重新查询');
    }
  };

  function reloadTable() {
    actionRef.value.reload();
  }

  function onCheckedRow(rowKeys) {
    console.log(rowKeys);
  }

  function onEditChange({ column, value, record }) {
    if (column.key === 'id') {
      record.editValueRefs.name4.value = `${value}`;
    }
    console.log(column, value, record);
  }

  // action
  function handleEdit(record) {
    showEditModal.value = true;
    editFormParams.user_id = record.user_id;
    editFormParams.name = record.name;
    editFormParams.nick_name = record.nick_name;
    editFormParams.phone = record.phone;
    editFormParams.sex = record.sex;
    editFormParams.status = record.status;
    editFormParams.role = record.role;
    currentEditKeyRef.value = record.key;
    record.onEdit?.(true);
  }

  async function handleSave() {
    const res = await editUser({ ...editFormParams });
    if (res.code == ResultEnum.SUCCESS) {
      window['$message'].info('用户信息修改成功');
      showEditModal.value = false;
      reloadTable();

      return res;
    } else {
      window['$message'].error('用户信息修改失败, 请重新输入');
    }
  }

  async function handleDelete(record: Recordable) {
    console.log('点击了删除', record);
    const res = await deleteUser({ ...record });
    if (res.code == 200) {
      window['$message'].info('用户信息删除成功');
      reloadTable();
      return res;
    } else {
      window['$message'].error('用户信息删除失败, 请检查操作');
    }
    reloadTable();
  }

  function handleCancel(record) {
    currentEditKeyRef.value = '';
    record.onEdit?.(false, false);
  }

  async function handleSubmit(values: Recordable) {
    schemasParams.name = values.name;
    schemasParams.phone = values.phone;
    schemasParams.status = values.status;
    schemasParams.sex = values.sex;
    reloadTable();
  }

  function handleReset(values: Recordable) {
    console.log(values);
  }

  function add() {
    showModal.value = true;
  }

  function confirmForm(e) {
    e.preventDefault();
    formBtnLoading.value = true;
    formRef.value.validate((errors) => {
      if (!errors) {
        addUser(formParams);
        reloadTable();
        window['$message'].success('添加用户成功');
        // 关闭弹窗
        setTimeout(() => {
          showModal.value = false;
        });
      } else {
        window['$message'].error('请填写完整信息');
      }
      clearFormParams();
      formBtnLoading.value = false;
    });
  }

  function clearFormParams() {
    for (const key in formParams) {
      formParams[key] = '';
    }
  }

  function createActions(record) {
    if (!record.editable) {
      return [
        {
          label: '编辑',
          onClick: handleEdit.bind(null, record),
        },
        {
          label: '删除',
          onClick: handleDelete.bind(null, record),
        },
      ];
    } else {
      return [
        {
          label: '保存',
          onClick: handleSave.bind(null, record),
        },
        {
          label: '取消',
          onClick: handleCancel.bind(null, record),
        },
      ];
    }
  }
</script>

<style lang="less" scoped></style>
