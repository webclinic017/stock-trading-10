export const columns = [
  {
    title: '股票代码',
    key: 'ts_code',
    width: 100,
  },
  {
    title: '购入价格',
    key: 'deal_price',
    width: 100,
  },
  {
    title: '持仓数量 ',
    key: 'number',
    width: 100,
  },
  {
    title: '购入成本',
    key: 'cost',
    width: 100,
  },
  {
    title: '当前市场价格 ',
    key: 'market_price',
    width: 100,
  },
  {
    title: '当前市值 ',
    key: 'market_value',
    width: 100,
  },
  {
    title: '盈亏情况',
    key: 'profit_loss',
    width: 100,
  },
  {
    title: '成交时间',
    key: 'deal_time',
    width: 100,
    render(row) {
      const date = new Date(row.deal_time);
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      return year + '.' + month + '.' + day;
    },
  },
];
