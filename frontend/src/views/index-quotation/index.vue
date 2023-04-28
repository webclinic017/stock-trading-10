<template>
  <n-card :bordered="false" class="proCard">
    <BasicForm @register="register" @submit="handleSubmit" @reset="handleReset">
      <template #statusSlot="{ model, field }">
        <n-input v-model:value="model[field]" />
      </template>
    </BasicForm>
    <n-card :bordered="false" class="proCard">
      <div>
        <NRow :gutter="24">
          <NCol :span="24">
            <n-card content-style="padding: 0;" :bordered="false">
              <n-tabs type="line" size="large" :tabs-padding="20" pane-style="padding: 20px;">
                <n-tab-pane name="日线行情">
                  <DailyKLine
                    :series="chartsParams.dailySeriesData"
                    :x-axis="chartsParams.dailyXAxisData"
                  />
                </n-tab-pane>
                <n-tab-pane name="周线行情">
                  <WeeklyKLine
                    :series="chartsParams.weeklySeriesData"
                    :x-axis="chartsParams.weeklyXAxisData"
                  />
                </n-tab-pane>
                <n-tab-pane name="月线行情">
                  <MonthlyKLine
                    :series="chartsParams.monthlySeriesData"
                    :x-axis="chartsParams.monthlyXAxisData"
                  />
                </n-tab-pane>
              </n-tabs>
            </n-card>
          </NCol>
        </NRow>
      </div>
    </n-card>
  </n-card>
</template>

<script lang="ts" setup>
  import { onMounted, reactive } from 'vue';
  import { BasicForm, FormSchema, useForm } from '@/components/Form';
  import DailyKLine from '@/views/index-quotation/components/DailyKLine.vue';
  import WeeklyKLine from '@/views/index-quotation/components/WeeklyKLine.vue';
  import MonthlyKLine from '@/views/index-quotation/components/MonthlyKLine.vue';
  import {
    getDailyKLine,
    getWeeklyKLine,
    getMonthlyKLine,
  } from '@/api/indexQuotation/index_quotation';
  import { ResultEnum } from '@/enums/httpEnum';
  const chartsParams = reactive({
    dailyXAxisData: [],
    dailySeriesData: [],
    weeklyXAxisData: [],
    weeklySeriesData: [],
    monthlyXAxisData: [],
    monthlySeriesData: [],
  });

  // schemas
  const schemasParams = reactive({
    ts_code: '000001.SH',
    start_date: 1609430400000,
    end_date: Date.now(),
  });
  const schemas: FormSchema[] = [
    {
      field: 'ts_code',
      component: 'NInput',
      label: '指数代码',
      defaultValue: '000001.SH',
      componentProps: {
        placeholder: '请输入指数代码',
        onInput: (e: any) => {
          console.log(e);
        },
      },
    },
    {
      field: 'start_date',
      component: 'NDatePicker',
      label: '开始日期',
      defaultValue: 1609430400000,
      componentProps: {
        type: 'date',
        clearable: true,
        onUpdateValue: (e: any) => {
          console.log(e);
        },
      },
    },
    {
      field: 'end_date',
      component: 'NDatePicker',
      label: '结束日期',
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

  onMounted(() => {
    handleSubmit(schemasParams);
  });
  async function handleSubmit(values: Recordable) {
    schemasParams.ts_code = values.ts_code;
    schemasParams.start_date = values.start_date;
    schemasParams.end_date = values.end_date;
    const [dailyData, weeklyData, monthlyData] = await Promise.all([
      getDailyKLine(schemasParams),
      getWeeklyKLine(schemasParams),
      getMonthlyKLine(schemasParams),
    ]);
    if (dailyData.code == ResultEnum.SUCCESS) {
      window['$message'].info('查询成功');
      chartsParams.dailyXAxisData = dailyData.result.trade_date_list;
      chartsParams.dailySeriesData = dailyData.result.data_list;
    } else {
      window['$message'].error('没有符合条件的日线行情数据, 请重新查询');
    }
    if (weeklyData.code == ResultEnum.SUCCESS) {
      window['$message'].info('查询成功');
      chartsParams.weeklyXAxisData = weeklyData.result.trade_date_list;
      chartsParams.weeklySeriesData = weeklyData.result.data_list;
    } else {
      window['$message'].error('没有符合条件的周线行情数据, 请重新查询');
    }
    if (monthlyData.code == ResultEnum.SUCCESS) {
      window['$message'].info('查询成功');
      chartsParams.monthlyXAxisData = monthlyData.result.trade_date_list;
      chartsParams.monthlySeriesData = monthlyData.result.data_list;
    } else {
      window['$message'].error('没有符合条件的月线行情数据, 请重新查询');
    }
  }

  function handleReset(values: Recordable) {
    schemasParams.ts_code = '';
    console.log(values);
  }
</script>

<style lang="less" scoped></style>
