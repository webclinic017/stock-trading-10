import os
from threading import Thread
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from backend.stock_trading.config import DB_URI
from backend.stock_trading.cron import update_market_value, get_dtl

db = SQLAlchemy()


def start_scheduler():
    # configure and initialize scheduler
    scheduler = BackgroundScheduler()
    # register cron job
    scheduler.add_job(update_market_value, 'interval', seconds=1)
    scheduler.add_job(get_dtl, 'cron', hour=18, minute=0)
    scheduler.start()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # TODO: 修改secret_key的值
    # init database
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import user, stock, position, order, dtl, quotation, index_quotation, account
    app.register_blueprint(user.user_bp)
    app.register_blueprint(stock.stock_bp)
    app.register_blueprint(position.position_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(dtl.dtl_bp)
    app.register_blueprint(quotation.quotation_bp)
    app.register_blueprint(index_quotation.index_quotation_bp)
    app.register_blueprint(account.account_bp)

    Thread(target=start_scheduler).start()

    return app
