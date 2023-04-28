import backtrader as bt
import pandas as pd
import tushare as ts
from backend.stock_trading.config import TOKEN

pro = ts.pro_api(TOKEN)


# 将tushare数据转换成框架想要用的数据
def prepare_tushare_data(ts_code='000001.SZ', start_date='20180701', end_date='20180718'):
    df = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
    df['date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d', utc=True)
    df['openinterest'] = 0
    df['volume'] = df['vol']
    return df[['date', 'open', 'high', 'low', 'close', 'volume', 'openinterest']]


class TestStrategy(bt.Strategy):
    params = (
        # 持仓够5个单位就卖出
        ('maperiod', 5),
    )

    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = dt or self.datas[0].datetime.date(0)
        log_message = '%s, %s' % (dt.isoformat(), txt)
        self.log_buffer.append(log_message)  # 将日志消息添加到缓冲区
        print(log_message)  # 在控制台打印日志消息

    def __init__(self):
        self.log_buffer = []  # 用于保存日志消息的列表
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close
        # 跟踪挂单
        self.order = None
        # 买入价格和手续费
        self.buyprice = None
        self.buycomm = None
        # 加入均线指标
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

    # 订单状态通知，买入卖出都是下单
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # broker 提交/接受了，买/卖订单则什么都不做
            return
        # 检查一个订单是否完成
        # 注意：当资金不足时，broker会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '已买入, 价格: %.2f, 费用: %.2f, 佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    '已卖出, 价格: %.2f, 费用: %.2f, 佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,  # 这个值是买股票时的价格？
                     order.executed.comm))
            # 记录当前交易数量
            self.bar_excuted = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')
        # 其他状态记录为：无挂起订单
        self.order = None

    # 交易状态通知，一买一卖算交易
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('交易利润，毛利润 %.2f,净利润 %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])

        # 如果有订单正在挂起，不操作
        if self.order:  # 什么情况挂起订单？
            return

        # 如果没有持仓则买入
        if not self.position:
            # 今天的收盘价在均线价格之上
            if self.dataclose[0] > self.sma[0]:
                # 买入
                self.log('买入单, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            # 如果已经持仓，收盘价在均线价格之下
            if self.dataclose[0] < self.sma[0]:
                # 全部卖出
                self.log('卖出单，%.2f' % self.dataclose[0])
                # 跟踪订单避免重复
                self.order = self.sell()


def backtest(ts_code='000001.SZ', start_date='20180701', end_date='20180718', cash=1000.0):
    # 创建Cerebro引擎
    cerebro = bt.Cerebro()
    # Cerebro引擎在后台创建broker(经纪人)，系统默认资金量为10000
    # 为Cerebro引擎添加策略
    cerebro.addstrategy(TestStrategy)

    # 创建交易数据集
    pandas_data = prepare_tushare_data(ts_code, start_date, end_date)
    pandas_data.set_index('date', inplace=True)
    pandas_data = pandas_data.iloc[::-1]  # 反转行
    data = bt.feeds.PandasData(dataname=pandas_data)  # 数据按时间逆序排列，会有影响吗？
    # 加载交易数据
    cerebro.adddata(data)
    # 设置投资金额100000.0
    # cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcash(cash)
    # 设置佣金为0.001
    # cerebro.broker.setcommission(commission=0.001)
    cerebro.broker.setcommission(commission=0.0)
    # 每笔交易使用固定交易量
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    # 引擎运行前打印期出资金
    print('组合期初资金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    strategy = cerebro.run()[0]  # 获取策略实例

    # 引擎运行后打期末资金
    print('组合期末资金: %.2f' % cerebro.broker.getvalue())
    return cerebro.broker.getvalue(), '\n'.join(strategy.log_buffer)


if __name__ == '__main__':
    final_money, log = backtest(ts_code='000001.SZ', start_date='20180701', end_date='20180718', cash=1000.0)
    print(">>>>>>>", log)
