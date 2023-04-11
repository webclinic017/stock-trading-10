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
  import { reactive, ref } from 'vue';
  import { BasicTable } from '@/components/Table';
  import { BasicForm, FormSchema, useForm } from '@/components/Form/index';
  import { columns } from './columns';
  import { ResultEnum } from '@/enums/httpEnum';
  import { getOrderList } from '@/api/order/order';
  const actionRef = ref();

  // schemas
  const schemasParams = reactive({
    order_no: '',
    status: '',
    type: '',
  });
  const schemas: FormSchema[] = [
    {
      field: 'order_no',
      component: 'NInput',
      label: '订单编号',
      componentProps: {
        placeholder: '请输入订单编号',
        onInput: (e: any) => {
          console.log(e);
        },
      },
    },
    {
      field: 'type',
      component: 'NSelect',
      label: '订单类型',
      componentProps: {
        placeholder: '请选择订单类型',
        options: [
          { label: '买入', value: 'buy' },
          { label: '卖出', value: 'sell' },
        ],
      },
    },
    {
      field: 'status',
      component: 'NSelect',
      label: '订单状态',
      componentProps: {
        placeholder: '请选择订单状态',
        options: [
          { label: '开始', value: 'start' },
          { label: '完成', value: 'finished' },
          { label: '异常', value: 'exception' },
        ],
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
    const data = await getOrderList({ ...res, ...schemasParams });
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
    schemasParams.order_no = values.order_no;
    schemasParams.status = values.status;
    schemasParams.type = values.type;
    reloadTable();
  }

  function handleReset(values: Recordable) {
    console.log(values);
  }
</script>

<style lang="less" scoped></style>
