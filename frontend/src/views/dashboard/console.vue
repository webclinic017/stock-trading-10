<template>
  <div class="console">
    <n-grid cols="1 s:2 m:3 " responsive="screen" :x-gap="12" :y-gap="8">
      <n-grid-item>
        <NCard
          title="当前资产"
          :segmented="{ content: true, footer: true }"
          size="small"
          :bordered="false"
        >
          <template #header-extra>
            <n-tag type="success">CNY</n-tag>
          </template>
          <div class="py-1 px-1 flex justify-between">
            <n-skeleton v-if="loading" :width="100" size="medium" />
            <CountTo prefix="￥" v-else :startVal="1" :endVal="account.asset" class="text-3xl" />
          </div>
          <div class="py-2 px-2 flex justify-between">
            <div class="text-sn flex-1">
              <n-progress
                type="line"
                :percentage="(account.asset * 100) / 20000"
                :indicator-placement="'inside'"
                processing
              />
            </div>
          </div>
          <template #footer>
            <div class="flex justify-between">
              <n-skeleton v-if="loading" text :repeat="2" />
              <template v-else>
                <div class="text-sn"> 可用现金：</div>
                <div class="text-sn">
                  <CountTo prefix="￥" :startVal="1" :endVal="account.money_rest" />
                </div>
              </template>
            </div>
          </template>
        </NCard>
      </n-grid-item>
      <n-grid-item>
        <NCard
          title="持仓情况"
          :segmented="{ content: true, footer: true }"
          size="small"
          :bordered="false"
        >
          <template #header-extra>
            <n-tag type="info">手</n-tag>
          </template>
          <div class="py-1 px-1 flex justify-between">
            <n-skeleton v-if="loading" :width="100" size="medium" />
            <CountTo
              v-else
              prefix="￥"
              :startVal="1"
              :endVal="position.market_value"
              class="text-3xl"
            />
          </div>
          <div class="flex justify-between" style="margin-top: 8px">
            <n-skeleton v-if="loading" :width="100" size="medium" />
            <template v-else>
              <div class="text-sn"> 持仓数量：</div>
              <div class="text-sn">
                <CountTo :startVal="1" :endVal="position.count" />
              </div>
            </template>
          </div>
          <template #footer>
            <div class="flex justify-between">
              <n-skeleton v-if="loading" :width="100" size="medium" />
              <template v-else>
                <div class="text-sn"> 盈亏情况：</div>
                <div class="text-sn">
                  <CountTo prefix="￥" :startVal="1" :endVal="position.profit_loss" />
                </div>
              </template>
            </div>
          </template>
        </NCard>
      </n-grid-item>
      <n-grid-item>
        <NCard
          title="订单量"
          :segmented="{ content: true, footer: true }"
          size="small"
          :bordered="false"
        >
          <template #header-extra>
            <n-tag type="info">个</n-tag>
          </template>
          <div class="py-1 px-1 flex justify-between">
            <n-skeleton v-if="loading" :width="100" size="medium" />
            <CountTo v-else prefix="￥" :startVal="1" :endVal="order.deal_value" class="text-3xl" />
          </div>
          <div class="py-2 px-2 flex justify-between">
            <div class="text-sn flex-1">
              <n-progress
                type="line"
                :percentage="(order.buy_count * 100) / order.count"
                :indicator-placement="'inside'"
                processing
              />
            </div>
          </div>
          <template #footer>
            <div class="flex justify-between">
              <n-skeleton v-if="loading" :width="100" size="medium" />
              <template v-else>
                <div class="text-sn"> 订单总量：</div>
                <div class="text-sn">
                  <CountTo :startVal="1" :endVal="order.count" />
                </div>
              </template>
            </div>
          </template>
        </NCard>
      </n-grid-item>
    </n-grid>

    <VisiTab />
  </div>
</template>
<script lang="ts" setup>
  import { onMounted, ref } from 'vue';
  import { getAccount, getOrder, getPosition } from '@/api/dashboard/console';
  import VisiTab from '@/views/dashboard/components/VisiTab.vue';
  import { CountTo } from '@/components/CountTo';
  import { ResultEnum } from '@/enums/httpEnum';

  const loading = ref(true);
  const account = ref({
    asset: 0.0,
    money_rest: 0.0,
  });
  const position = ref({
    count: 0.0,
    market_value: 0.0,
    profit_loss: 0.0,
  });
  const order = ref({
    count: 0.0,
    deal_value: 0.0,
    buy_count: 0.0,
  });

  onMounted(async () => {
    loading.value = true;
    const [accountData, positionData, orderData] = await Promise.all([
      getAccount(),
      getPosition(),
      getOrder(),
    ]);
    if (accountData.code == ResultEnum.SUCCESS) {
      window['$message'].info('账户信息查询成功');
      account.value.asset = accountData.result.asset;
      account.value.money_rest = accountData.result.money_rest;
    } else {
      window['$message'].error('账户信息查询失败, 请检查');
    }
    if (positionData.code == ResultEnum.SUCCESS) {
      window['$message'].info('持仓信息查询成功');
      position.value.count = positionData.result.count;
      position.value.market_value = positionData.result.market_value;
      position.value.profit_loss = positionData.result.profit_loss;
    } else {
      window['$message'].error('持仓信息查询失败, 请检查');
    }
    if (orderData.code == ResultEnum.SUCCESS) {
      window['$message'].info('订单信息查询成功');
      order.value.count = orderData.result.count;
      order.value.deal_value = orderData.result.deal_value;
      order.value.buy_count = orderData.result.buy_count;
    } else {
      window['$message'].error('订单信息查询失败, 请检查');
    }
    loading.value = false;
  });
</script>

<style lang="less" scoped></style>
