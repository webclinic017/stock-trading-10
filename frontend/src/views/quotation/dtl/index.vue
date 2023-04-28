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
  import { onMounted, reactive, ref } from 'vue';
  import { BasicTable } from '@/components/Table';
  import { BasicForm, FormSchema, useForm } from '@/components/Form';
  import { columns } from './columns';
  import { ResultEnum } from '@/enums/httpEnum';
  import { getDtlInfo } from '@/api/quotation/quotation';
  import { getStockNames } from '@/api/stock/stock';

  const actionRef = ref();
  let stockNames = [];
  const validatorTsCode = (rule, value, callback) => {
    if (!value) {
      callback();
      return;
    }
    const regex = /^\d{6}(\.(SH|SZ))?$/;
    if (regex.test(value)) {
      callback();
    } else {
      callback(new Error('请输入正确的股票代码，比如000001.SZ'));
    }
  };
  const validatorStockName = (rule, value, callback) => {
    if (!value) {
      callback();
      return;
    }
    if (stockNames.includes(value)) {
      callback();
    } else {
      callback(new Error('请输入正确的股票名称'));
    }
  };

  // schemas
  const schemasParams = reactive({
    ts_code: '',
    name: '',
    trade_date: Date.now(),
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
      rules: [{ validator: validatorTsCode, trigger: ['blur', 'input'] }],
    },
    {
      field: 'name',
      component: 'NInput',
      label: '股票名称',
      componentProps: {
        placeholder: '请输入股票名称',
        onInput: (e: any) => {
          console.log(e);
        },
      },
      rules: [{ validator: validatorStockName, trigger: ['blur', 'input']}],
    },
    {
      field: 'trade_date',
      component: 'NDatePicker',
      label: '交易日期',
      defaultValue: Date.now(),
      componentProps: {
        type: 'date',
        clearable: true,
        onUpdateValue: (e: any) => {
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

  // table
  const loadDataTable = async (res) => {
    const data = await getDtlInfo({ ...res, ...schemasParams });
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
    schemasParams.trade_date = values.trade_date;
    reloadTable();
  }

  function handleReset(values: Recordable) {
    console.log(values);
  }
  onMounted(() => {
    getStocks();
  });
  async function getStocks() {
    const res = await getStockNames();
    if (res.code == ResultEnum.SUCCESS) {
      stockNames = res.result.stock_name;
    }
  }
</script>

<style lang="less" scoped></style>
