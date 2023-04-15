<template>
  <div>
    <div class="n-layout-page-header">
      <n-card :bordered="false" title="公司简介">{{ company.introduction }}</n-card>
      <n-card :bordered="false" title="主营业务">{{ company.main_business }}</n-card>
    </div>
    <n-card :bordered="false" class="proCard mt-4" :segmented="{ content: true }">
      <n-descriptions label-placement="left" class="py-2">
        <n-descriptions-item label="交易所">{{ company.exchange }}</n-descriptions-item>
        <n-descriptions-item label="法人代表">{{ company.chairman }}</n-descriptions-item>
        <n-descriptions-item label="注册资本">{{ company.reg_capital }}</n-descriptions-item>
        <n-descriptions-item label="公司主页">{{ company.website }}</n-descriptions-item>
      </n-descriptions>
    </n-card>
  </div>
</template>

<script>
  import { getCompanyInfo } from '@/api/company/company';
  import { ResultEnum } from '@/enums/httpEnum';

  export default {
    data() {
      return {
        company: {
          ts_code: '',
          exchange: '',
          chairman: '',
          reg_capital: '',
          introduction: '',
          website: '',
          main_business: '',
        },
        params: {
          ts_code: '',
        },
      };
    },
    beforeMount() {
      this.params.ts_code = this.$route.params.ts_code;
      this.loadCompanyInfo();
    },
    methods: {
      async loadCompanyInfo() {
        const data = await getCompanyInfo(this.params);
        if (data.code === ResultEnum.SUCCESS) {
          window['$message'].info('查询成功');
          this.company.ts_code = data.result.ts_code;
          this.company.exchange = data.result.exchange;
          this.company.chairman = data.result.chairman;
          this.company.reg_capital = data.result.reg_capital;
          this.company.introduction = data.result.introduction;
          this.company.website = data.result.website;
          this.company.main_business = data.result.main_business;
        } else {
          window['$message'].error('没有符合条件的数据, 请重新查询');
        }
      },
    },
  };
</script>

<style lang="less" scoped></style>
