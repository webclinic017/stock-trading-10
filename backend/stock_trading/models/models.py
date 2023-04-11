from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import DateTime, Float, ForeignKey, String


class BaseModel:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Base(DeclarativeBase):
    pass


class User(Base, BaseModel):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    nick_name: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    sex: Mapped[str] = mapped_column(String(255))
    create_time: Mapped[DateTime] = mapped_column(DateTime)
    update_time: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))
    account_id = mapped_column(ForeignKey('account.account_id'), index=True)

    account = relationship('Account')


class Account(Base, BaseModel):
    __tablename__ = 'account'

    account_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    asset: Mapped[float] = mapped_column(Float())
    market_value: Mapped[float] = mapped_column(Float())
    money_rest: Mapped[float] = mapped_column(Float())


class Position(Base, BaseModel):
    __tablename__ = 'position'

    position_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    account_id: Mapped[int] = mapped_column(INTEGER(11))
    ts_code: Mapped[str] = mapped_column(String(255))
    deal_price: Mapped[float] = mapped_column(Float())
    number: Mapped[float] = mapped_column(Float())
    cost: Mapped[float] = mapped_column(Float())
    market_price: Mapped[float] = mapped_column(Float())
    market_value: Mapped[float] = mapped_column(Float())
    profit_loss: Mapped[float] = mapped_column(Float())
    deal_time: Mapped[DateTime] = mapped_column(DateTime)


class Stock(Base, BaseModel):
    __tablename__ = 'stock'

    ts_code: Mapped[str] = mapped_column(String(255), primary_key=True)
    symbol: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    area: Mapped[str] = mapped_column(String(255))
    industry: Mapped[str] = mapped_column(String(255))
    market: Mapped[str] = mapped_column(String(255))
    exchange: Mapped[str] = mapped_column(String(255))


class Order(Base, BaseModel):
    __tablename__ = 'order'

    order_no: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[int] = mapped_column(INTEGER(11))
    ts_code: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    deal_price: Mapped[float] = mapped_column(Float())
    deal_number: Mapped[float] = mapped_column(Float())
    deal_value: Mapped[float] = mapped_column(Float())
    deal_date: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(255))


class Company(Base, BaseModel):
    __tablename__ = 'company'

    company_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    chairman: Mapped[str] = mapped_column(String(255))
    reg_capital: Mapped[str] = mapped_column(String(255))
    introduction: Mapped[str] = mapped_column(String(255))
    website: Mapped[str] = mapped_column(String(255))
    main_business: Mapped[str] = mapped_column(String(255))


class Dtl(Base, BaseModel):
    __tablename__ = 'dtl'

    dtl_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    ts_code: Mapped[str] = mapped_column(String(255))
    trade_date: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    close: Mapped[float] = mapped_column(Float())
    pct_change: Mapped[float] = mapped_column(Float())
    turnover_rate: Mapped[float] = mapped_column(Float())
    amount: Mapped[float] = mapped_column(Float())
    l_sell: Mapped[float] = mapped_column(Float())
    l_buy: Mapped[float] = mapped_column(Float())
    l_amount: Mapped[float] = mapped_column(Float())
    net_amount: Mapped[float] = mapped_column(Float())
    net_rate: Mapped[float] = mapped_column(Float())
    amount_rate: Mapped[float] = mapped_column(Float())
    float_values: Mapped[float] = mapped_column(Float())
    reason: Mapped[str] = mapped_column(String(255))

