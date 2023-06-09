export const columns = [
  {
    title: '订单编号',
    key: 'order_no',
    width: 100,
  },
  {
    title: '股票代码',
    key: 'ts_code',
    width: 100,
  },
  {
    title: '交易类型',
    key: 'type',
    width: 100,
  },
  {
    title: '成交价格',
    key: 'deal_price',
    width: 100,
  },
  {
    title: '成交数量 ',
    key: 'deal_number',
    width: 100,
  },
  {
    title: '成交金额',
    key: 'deal_value',
    width: 100,
  },
  {
    title: '成交时间',
    key: 'deal_date',
    width: 100,
    render(row) {
      const date = new Date(row.deal_date);
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      return year + '.' + month + '.' + day;
    },
  },
  {
    title: '订单状态',
    key: 'status',
    width: 100,
  },
];
