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
          购买股票
        </n-button>
      </template>
      <template #toolbar>
        <n-button type="primary" @click="reloadTable">刷新数据</n-button>
      </template>
    </BasicTable>

    <n-modal v-model:show="showModal" :show-icon="false" preset="dialog" title="购买股票">
      <n-form
        :model="formParams"
        :rules="formRules"
        ref="formRef"
        label-placement="left"
        :label-width="80"
        class="py-4"
      >
        <n-form-item label="股票代码" path="ts_code">
          <n-input
            placeholder="请输入股票代码"
            v-model:value="formParams.ts_code"
            @blur="onInputBlur"
          />
        </n-form-item>
        <n-form-item label="市场价格" path="deal_price">
          <n-input placeholder="" v-model:value="formParams.market_price" disabled />
        </n-form-item>
        <n-form-item label="购入数量" path="number">
          <n-input placeholder="请输入购入数量" v-model:value="formParams.number" />
        </n-form-item>
      </n-form>

      <template #action>
        <n-space>
          <n-button @click="() => (showModal = false)">取消</n-button>
          <n-button type="info" :loading="formBtnLoading" @click="confirmForm">确定</n-button>
        </n-space>
      </template>
    </n-modal>
    <n-modal v-model:show="showSellModal" :show-icon="false" preset="dialog" title="卖出股票">
      <n-form
        :model="sellFormParams"
        :rules="sellFormRules"
        ref="editFormRef"
        label-placement="left"
        :label-width="80"
        class="py-4"
      >
        <n-form-item label="股票代码" path="name">
          <n-input v-model:value="sellFormParams.ts_code" disabled />
        </n-form-item>
        <n-form-item label="买入价格" path="deal_price">
          <n-input v-model:value="sellFormParams.deal_price" disabled />
        </n-form-item>
        <n-form-item label="市场价格" path="market_price">
          <n-input v-model:value="sellFormParams.market_price" disabled />
        </n-form-item>
        <n-form-item label="差额" path="difference">
          <n-input v-model:value="sellFormParams.difference" disabled />
        </n-form-item>
        <n-form-item label="股票数量" path="number">
          <n-input v-model:value="sellFormParams.number" disabled />
        </n-form-item>
        <n-form-item label="卖出数量" path="sell_number">
          <n-input v-model:value="sellFormParams.sell_number" />
        </n-form-item>
      </n-form>

      <template #action>
        <n-space>
          <n-button @click="() => (showModal = false)">取消</n-button>
          <n-button type="info" :loading="formBtnLoading" @click="handleSave">卖出</n-button>
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
  import { buyStock, getMarketPrice, getPositionInfo, sellStock } from '@/api/stock/stock';

  const formRef: any = ref(null);
  const editFormRef: any = ref(null);
  const actionRef = ref();
  const currentEditKeyRef = ref('');
  const showModal = ref(false);
  const showSellModal = ref(false);
  const formBtnLoading = ref(false);
  const passInspect = ref(false);

  const formParams = reactive({
    ts_code: '',
    market_price: '',
    number: '',
    availableNumber: NaN,
  });
  // form
  const formRules: FormRules = {
    ts_code: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入股票代码',
      },
      {
        validator: (rule, value) => {
          const regex = /^\d{6}(\.(SH|SZ))?$/;
          if (regex.test(value)) {
            passInspect.value = true;
            return Promise.resolve();
          }
          return Promise.reject(new Error('请输入正确的股票代码, 比如000001.SZ'));
        },
        trigger: ['blur', 'input'],
      },
    ],
    number: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入购入数量',
      },
      {
        validator: (rule, value) => {
          const min = 1;
          const max = formParams.availableNumber;
          if (value < min || value > max) {
            return Promise.reject(new Error(`购入数量必须在1和${formParams.availableNumber}之间`));
          }
          return true;
        },
        trigger: ['blur', 'input'],
      },
    ],
  };
  const sellFormParams = reactive({
    ts_code: '',
    deal_price: '',
    number: '',
    market_price: '',
    sell_number: '',
    difference: '',
  });
  const sellFormRules: FormRules = {
    sell_number: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入卖出数量',
      },
      {
        validator: (rule, value) => {
          const min = 1;
          const max = sellFormParams.number;
          if (value < min || value > max) {
            return Promise.reject(new Error(`购入数量必须在1和${sellFormParams.number}之间`));
          }
          return true;
        },
        trigger: ['blur', 'input'],
      },
    ],
  };

  const schemasParams = reactive({
    ts_code: '',
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
  ];

  const [register, {}] = useForm({
    gridProps: { cols: '1 s:1 m:2 l:3 xl:4 2xl:4' },
    labelWidth: 80,
    schemas,
  });

  // action
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
    const data = await getPositionInfo({ ...res, ...schemasParams });
    if (data.code == ResultEnum.SUCCESS) {
      window['$message'].info('查询成功');
      return data.result;
    } else {
      window['$message'].error('没有符合条件的数据, 请重新查询');
    }
  };

  async function onInputBlur() {
    if (passInspect.value) {
      const data = await getMarketPrice(formParams);
      if (data.code == ResultEnum.SUCCESS) {
        formParams.market_price = data.result.market_price;
        formParams.availableNumber = Math.floor(data.result.money_rest / data.result.market_price);
        window['$message'].info(`当前股票的市场价格是${formParams.market_price}`);
        window['$message'].info(
          `当前余额是是${data.result.money_rest}, 最多可购入 ${formParams.availableNumber} 股`
        );
        passInspect.value = false;
      } else {
        window['$message'].error('当前不是交易日，请择日购入');
      }
    }
  }
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
  function handleSell(record) {
    showSellModal.value = true;
    sellFormParams.ts_code = record.ts_code;
    sellFormParams.deal_price = record.deal_price;
    sellFormParams.number = record.number;
    sellFormParams.market_price = record.market_value / record.number;
    sellFormParams.difference = sellFormParams.market_price - sellFormParams.deal_price;
    record.onEdit?.(true);
  }

  async function handleSave() {
    const res = await sellStock({ ...sellFormParams });
    if (res.code == ResultEnum.SUCCESS) {
      window['$message'].info('股票卖出成功');
      showSellModal.value = false;
      reloadTable();
      clearSellFormParams();
      return res;
    } else {
      window['$message'].error('股票卖出失败, 请检查数据');
    }
  }

  function handleCancel(record) {
    currentEditKeyRef.value = '';
    record.onEdit?.(false, false);
  }

  async function handleSubmit(values: Recordable) {
    schemasParams.ts_code = values.ts_code;
    reloadTable();
  }

  function handleReset(values: Recordable) {
    console.log(values);
  }

  function add() {
    showModal.value = true;
    clearFormParams();
  }

  function confirmForm(e) {
    e.preventDefault();
    formBtnLoading.value = true;
    formRef.value.validate(async (errors) => {
      if (!errors) {
        const data = await buyStock(formParams);
        if (data.code == ResultEnum.SUCCESS) {
          window['$message'].info('股票购买成功');
        } else {
          window['$message'].error('股票购买失败, 请检查操作');
        }
        reloadTable();
        // 关闭弹窗
        setTimeout(() => {
          showModal.value = false;
        });
      } else {
        window['$message'].error('');
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
  function clearSellFormParams() {
    for (const key in sellFormParams) {
      sellFormParams[key] = '';
    }
  }
  function createActions(record) {
    if (!record.editable) {
      return [
        {
          label: '卖出',
          onClick: handleSell.bind(null, record),
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
