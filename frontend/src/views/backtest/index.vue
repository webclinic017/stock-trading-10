<template>
  <div>
    <BasicForm @register="register" @submit="handleSubmit" @reset="handleReset">
      <template #statusSlot="{ model, field }">
        <n-input v-model:value="model[field]" />
      </template>
    </BasicForm>
    <n-card :bordered="false" title="期末资金">{{ params.end_cash }}</n-card>
  </div>
</template>

<script lang="ts" setup>
  import { BasicForm, FormSchema, useForm } from '@/components/Form';
  import { ResultEnum } from '@/enums/httpEnum';
  import { getBackTestInfo } from '@/api/backtest/backtest';
  import { reactive } from 'vue';

  const params = reactive({
    end_cash: 0,
  });

  // schemas
  const schemasParams = reactive({
    ts_code: '000001.SH',
    cash: 1000000,
    start_date: 1609430400000,
    end_date: Date.now(),
  });
  const schemas: FormSchema[] = [
    {
      field: 'ts_code',
      component: 'NInput',
      label: '指数代码',
      defaultValue: '000001.SZ',
      componentProps: {
        placeholder: '请输入指数代码',
        onInput: (e: any) => {
          console.log(e);
        },
      },
      rules: [{ required: true, trigger: ['blur', 'input'] }],
    },
    {
      field: 'cash',
      component: 'NInput',
      label: '初始资金',
      defaultValue: '10000',
      componentProps: {
        placeholder: '请输入初始资金',
        onInput: (e: any) => {
          console.log(e);
        },
      },
      rules: [{ required: true, trigger: ['blur', 'input'] }],
    },
    {
      field: 'start_date',
      component: 'NDatePicker',
      label: '开始日期',
      defaultValue: 1530374400000,
      componentProps: {
        type: 'date',
        clearable: true,
        onUpdateValue: (e: any) => {
          console.log(e);
        },
      },
      rules: [{ required: true, trigger: ['blur', 'input'] }],
    },
    {
      field: 'end_date',
      component: 'NDatePicker',
      label: '结束日期',
      defaultValue: 1531843200000,
      componentProps: {
        type: 'date',
        clearable: true,
        onUpdateValue: (e: any) => {
          console.log(e);
        },
      },
      rules: [{ required: true, trigger: ['blur', 'input'] }],
    },
  ];
  const [register, {}] = useForm({
    gridProps: { cols: '1 s:1 m:2 l:3 xl:4 2xl:4' },
    labelWidth: 80,
    schemas,
  });
  async function handleSubmit(values: Recordable) {
    schemasParams.ts_code = values.ts_code;
    schemasParams.cash = values.cash;
    schemasParams.start_date = values.start_date;
    schemasParams.end_date = values.end_date;
    const data = await getBackTestInfo({ ...schemasParams });
    if (data.code == ResultEnum.SUCCESS) {
      window['$message'].info('查询成功');
      params.end_cash = data.result.end_cash;
    } else {
      window['$message'].error('没有符合条件的数据, 请重新查询');
    }
  }

  function handleReset(values: Recordable) {
    schemasParams.ts_code = '';
    console.log(values);
  }
</script>

<style lang="less" scoped></style>