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
        <n-form-item label="购入数量" path="buy_number">
          <n-input placeholder="请输入购入数量" v-model:value="formParams.buy_number" />
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
        <n-form-item label="股票持有数量" path="hold_number">
          <n-input v-model:value="sellFormParams.hold_number" disabled />
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
    buy_number: '',
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
    buy_number: [
      {
        required: true,
        trigger: ['blur', 'input'],
        message: '请输入购入数量',
      },
      {
        validator: (rule, value) => {
          if (formParams.ts_code.substring(0, 3) === '688') {
            if (formParams.availableNumber < 200) {
              return Promise.reject(new Error('余额不足 无法购入'));
            }
            const min = 200;
            const max = formParams.availableNumber;
            if (value < min || value > max) {
              return Promise.reject(
                new Error(`购入数量最少为200，且必须在200和${formParams.availableNumber}之间`)
              );
            }
            return true;
          } else {
            if (formParams.availableNumber < 100) {
              return Promise.reject(new Error('余额不足 无法购入'));
            }
            const min = 100;
            const max = formParams.availableNumber;
            if (value < min || value > max || value % 100 !== 0) {
              return Promise.reject(
                new Error(
                  `购入数量以100的整数倍递增如100股、200股、300股，且必须在100和${formParams.availableNumber}之间`
                )
              );
            }
            return true;
          }
        },
        trigger: ['blur', 'input'],
      },
    ],
  };
  const sellFormParams = reactive({
    ts_code: '',
    deal_price: '',
    hold_number: '',
    market_price: '',
    sell_number: '',
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
          if (sellFormParams.ts_code.substring(0, 3) === '688') {
            if (parseInt(sellFormParams.hold_number) <= 200) {
              sellFormParams.sell_number = sellFormParams.hold_number;
              window['$message'].info('科创股少于200必须全部卖出');
              return true;
            } else {
              const min = 200;
              const max = sellFormParams.hold_number;
              if (value < min || value > max) {
                return Promise.reject(
                  new Error(`卖出数量最少为200，且必须在200和${sellFormParams.hold_number}之间`)
                );
              }
              return true;
            }
          } else {
            if (parseInt(sellFormParams.hold_number) <= 100) {
              sellFormParams.sell_number = sellFormParams.hold_number;
              window['$message'].info('非科创股少于100只股票必须全部卖出');
              return true;
            } else {
              const min = 100;
              const max = sellFormParams.hold_number;
              if (value < min || value > max) {
                return Promise.reject(
                  new Error(`卖出数量必须应在1至${sellFormParams.hold_number}之间`)
                );
              }
              return true;
            }
          }
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
    sellFormParams.hold_number = record.number;
    sellFormParams.market_price = record.market_price;
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
        clearFormParams();
        reloadTable();
        // 关闭弹窗
        setTimeout(() => {
          showModal.value = false;
        });
      } else {
        window['$message'].error('股票购买失败, 请检查数据');
      }
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
