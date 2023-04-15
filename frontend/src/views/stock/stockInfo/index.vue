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
      <template #toolbar>
        <n-button type="primary" @click="reloadTable">刷新数据</n-button>
      </template>
    </BasicTable>
  </n-card>
</template>

<script lang="ts" setup>
  import { h, reactive, ref } from 'vue';
  import { BasicTable, TableAction } from '@/components/Table';
  import { BasicForm, FormSchema, useForm } from '@/components/Form/index';
  import { columns } from './columns';
  import { ResultEnum } from '@/enums/httpEnum';
  import { getStockInfo } from '@/api/stock/stock';
  import { useRouter } from 'vue-router';
  const router = useRouter();
  const actionRef = ref();

  // schemas
  const schemasParams = reactive({
    ts_code: '',
    name: '',
    market: '',
  });
  const schemas: FormSchema[] = [
    {
      field: 'ts_code',
      component: 'NInput',
      label: 'TS代码',
      componentProps: {
        placeholder: '请输入TS代码',
        onInput: (e: any) => {
          console.log(e);
        },
      },
    },
    {
      field: 'name',
      component: 'NInput',
      label: '股票名称',
      componentProps: {
        placeholder: '请输入股票名称',
        showButton: false,
        onInput: (e: any) => {
          console.log(e);
        },
      },
    },
    {
      field: 'market',
      component: 'NInput',
      label: '市场类型',
      componentProps: {
        placeholder: '请输入市场类型',
        showButton: false,
        onInput: (e: any) => {
          console.log(e);
        },
      },
    },
  ];
  const [register, {}] = useForm({
    gridProps: { cols: '1 s:1 m:2 l:3 xl:4 2xl:4' },
    labelWidth: 80,
    schemas,
  });
  const actionColumn = reactive({
    width: 50,
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
    const data = await getStockInfo({ ...res, ...schemasParams });
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

  async function handleSubmit(values: Recordable) {
    schemasParams.ts_code = values.ts_code;
    schemasParams.name = values.name;
    schemasParams.market = values.market;
    reloadTable();
  }

  function handleReset(values: Recordable) {
    console.log(values);
  }
  function createActions(record) {
    return [
      {
        label: '详情',
        onClick: viewDetail.bind(null, record),
      },
    ];
  }
  function viewDetail(record: Recordable) {
    router.push({ name: 'company-info', params: { ts_code: record.ts_code } });
  }
</script>

<style lang="less" scoped></style>
