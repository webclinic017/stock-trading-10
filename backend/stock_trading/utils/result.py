from backend.stock_trading.models import User


class Result:
    def __init__(self):
        pass

    def as_dict(self):
        return {

        }


class PageResult(Result):
    def __init__(self, list=None, page=None, pageCount=None, pageSize=None):
        self.list = list
        self.page = page
        self.pageCount = pageCount
        self.pageSize = pageSize

    def as_dict(self):
        return {
            'list': self.list,
            'page': self.page,
            'pageCount': self.pageCount,
            'pageSize': self.pageSize,
        }


class TokenResult(Result):
    def __init__(self, token=None):
        self.token = token

    def as_dict(self):
        return {
            'token': self.token,
        }


class UserInfoResult(Result):
    def __init__(self, user=User, permissions=None):
        self.user = user
        self.permissions = permissions

    def as_dict(self):
        return {
            'user_id': self.user.user_id,
            'name': self.user.name,
            'nick_name': self.user.nick_name,
            'phone': self.user.phone,
            'password': self.user.password,
            'sex': self.user.sex,
            'create_time': self.user.create_time,
            'update_time': self.user.update_time,
            'status': self.user.status,
            'role': self.user.role,
            'account_id': self.user.account_id,
            'permissions': self.permissions,
        }


class MarketPriceResult(Result):
    def __init__(self, market_price=None, money_rest=None):
        self.market_price = market_price
        self.money_rest = money_rest

    def as_dict(self):
        return {
            'market_price': self.market_price,
            'money_rest': self.money_rest,
        }


class RealTimeResult(Result):
    def __init__(self, trade_date_list=None, data_list=None):
        self.trade_date_list = trade_date_list
        self.data_list = data_list

    def as_dict(self):
        return {
            'trade_date_list': self.trade_date_list,
            'data_list': self.data_list,
        }
