import time
import re
import tushare as ts
from sqlalchemy import create_engine
from backend.stock_trading.config import DB_URI, TOKEN

engine = create_engine(DB_URI)
pro = ts.pro_api(TOKEN)


# 按照时间生成订单号
def get_order_code():
    #  年月日时分秒+time.time()的后7位
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
    return order_no


# 通过股票代码前三位判断股票市场
def get_market(code_string):
    market_code_dict = {
        "600": "SH",  # 沪市A股
        "601": "SH",  # 沪市A股
        "603": "SH",  # 沪市A股
        "605": "SH",  # 沪市A股
        "000": "SZ",  # 深市A股
        "001": "SZ",  # 深市A股
        "003": "SZ",  # 深市A股
        "688": "IB",  # 科创板
        "300": "SZ",  # 创业板（旧）
        "301": "SZ",  # 创业板
        "002": "SZ",  # 中小板
    }
    return market_code_dict.get(code_string[:3], None)


# 调用tushare接口获取股票实时价格
def get_market_value(ts_code):
    regex = r'^(\d{6})(\.(SH|SZ))$'

    match = re.match(regex, ts_code)
    if match:
        ts_code = ts_code[:-3]
    df = ts.get_realtime_quotes(ts_code)
    if df is not None and not df.empty:
        market_value = df.iloc[0]['price']
    else:
        return 0
    return market_value


# init stock_list_info
def get_stock_info():
    df = pro.stock_basic(**{
        "ts_code": "",
        "name": "",
        "exchange": "",
        "market": "",
        "is_hs": "",
        "list_status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "symbol",
        "name",
        "area",
        "industry",
        "market",
        "exchange"
    ])

    df.to_sql(name='stock', con=engine, if_exists='replace', index=False)


# get long_hu_bang data
def get_long_hu_bang():
    df = pro.top_list(trade_date='20230407')
    df.to_sql(name='dtl', con=engine, if_exists='append', index=False)


def get_realtime_info():
    df = pro.daily(ts_code='000001.SZ', start_date='20230411', end_date='20230411')
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()

if __name__ == '__main__':
    get_realtime_info()
