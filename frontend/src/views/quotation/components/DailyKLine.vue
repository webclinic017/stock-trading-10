<template>
  <div class="echart" id="daily-kline" style="width: 100%; height: 500px"></div>
</template>

<script>
  import * as echarts from 'echarts';
  export default {
    props: {
      xAxis: {
        type: Array,
        default: function () {
          return [];
        },
      },
      series: {
        type: Array,
        default: function () {
          return [];
        },
      },
    },
    data() {
      return {};
    },
    mounted() {
      this.initEcharts();
    },
    updated() {
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
            data: ['日线行情'],
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
              name: '日线行情',
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
        const myChart = echarts.init(document.getElementById('daily-kline'), 'dark');
        myChart.setOption(option);
        window.addEventListener('resize', () => {
          myChart.resize();
        });
      },
    },
  };
</script>
