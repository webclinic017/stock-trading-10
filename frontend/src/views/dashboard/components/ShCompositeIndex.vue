<template>
  <div class="echart" id="daily-kline" style="width: 100%; height: 500px"></div>
</template>

<script>
  import * as echarts from 'echarts';
  import { getDailyKLine } from '@/api/indexQuotation/index_quotation';
  import { ResultEnum } from '@/enums/httpEnum';

  export default {
    data() {
      return {
        params: {
          ts_code: '000001.SH',
          start_date: 1609430400000,
          end_date: Date.now(),
        },
        xAxis: [],
        series: [],
      };
    },
    async mounted() {
      const data = await getDailyKLine(this.params);
      if (data.code === ResultEnum.SUCCESS) {
        this.xAxis = data.result.trade_date_list;
        this.series = data.result.data_list;
      }
      this.initEcharts();
    },
    methods: {
      initEcharts() {
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
            },
          },
          legend: {
            data: ['上证指数-日线行情'],
          },
          grid: [
            {
              left: '10%',
              right: '10%',
              height: '50%',
            },
            {
              left: '10%',
              right: '10%',
              top: '63%',
              height: '16%',
            },
          ],
          xAxis: {
            type: 'category',
            data: this.xAxis,
          },
          yAxis: {},
          series: [
            {
              name: '上证指数-日线行情',
              type: 'candlestick',
              data: this.series,
            },
          ],
          brush: {
            xAxisIndex: 'all',
            brushLink: 'all',
            outOfBrush: {
              colorAlpha: 0.1,
            },
          },
          dataZoom: [
            {
              type: 'inside',
              xAxisIndex: [0, 1],
              start: 0,
              end: 100,
            },
            {
              show: true,
              xAxisIndex: [0, 1],
              type: 'slider',
              top: '85%',
              start: 0,
              end: 100,
            },
          ],
        };
        const myChart = echarts.init(document.getElementById('daily-kline'));
        myChart.setOption(option);
        window.addEventListener('resize', () => {
          myChart.resize();
        });
      },
    },
  };
</script>
