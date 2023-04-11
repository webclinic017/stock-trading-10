import datetime

from sqlalchemy.exc import SQLAlchemyError
from backend.stock_trading.models import Account, Position
from backend.stock_trading.config import DB_URI, TOKEN
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.stock_trading.utils.util import get_market_value
import tushare as ts

pro = ts.pro_api(TOKEN)
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = Session()


def update_market_value():
    account_ids = [result[0] for result in session.query(Account.account_id).all()]
    for account_id in account_ids:
        positions = session.query(Position).filter_by(account_id=account_id).all()
        market_value_total = 0
        for position in positions:
            market_price = float(get_market_value(position.ts_code))
            position.market_price = market_price
            position.market_value = market_price * position.number
            position.profit_loss = position.market_value - position.cost
            market_value_total += position.market_value
        account = session.query(Account).filter_by(account_id=account_id).first()
        account.market_value = market_value_total
        account.asset = account.market_value + account.money_rest
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(">>> update market value failed >>>")
        else:
            pass
            # print(">>> update market value success >>>")
        finally:
            session.close()


# get long_hu_bang data
def get_dtl():
    df = pro.top_list(trade_date=datetime.datetime.now().strftime("%Y%m%d"))
    df.to_sql(name='dtl', con=engine, if_exists='append', index=False)
