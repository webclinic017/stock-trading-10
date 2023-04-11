# Stock-Trading

## 💾 简介

1、功能简介

- 利用该系统用户可以进行股票的模拟交易，其功能主要包括：股票行情(历史行情、实时行情、龙虎榜)、指数行情、股票基础信息用户持仓展示、股票买入和卖出、订单生成及检索、个人信息设置以及用户管理等功能。

2、技术栈

- 前端：`Vue3`、`Typescript`、`Pinia`、`Vite` 、`ant` 、`echarts` ；
- 后端：`Flask`、`SQLAlchemy`。

## 📝 使用

1、获取项目代码

```bash
git clone https://github.com/six-double-seven/stock-trading.git
```

2、前端

- 安装依赖

```bash
cd frontend

yarn install
```

- 运行

```bash
yarn dev
```

- 打包

```bash
yarn build
```

3、数据库

- 运行db/stock_trading.sql文件，创建数据库。

4、后端

- 修改config.py

```bash
cd backend/stock_trading/config.py

修改其中的数据库信息及Tushare数据源的TOKEN
```

- 启动项目

```bash
cd backend/stock_trading

$ export FLASK_APP=stock_trading
$ export FLASK_ENV=development
$ flask run
```

## 👏 贡献

1、Pull Request

- Fork 代码
- 创建自己的分支: `git checkout -b feat/xxxx`
- 提交你的修改: `git commit -am 'feat(function): add xxxxx'`
- 推送您的分支: `git push origin feat/xxxx`
- 提交`pull request`



2、Git 贡献提交规范

- `feat` 增加新功能
- `fix` 修复问题/BUG
- `style` 代码风格相关无影响运行结果的
- `perf` 优化/性能提升
- `refactor` 重构
- `revert` 撤销修改
- `test` 测试相关
- `docs` 文档/注释
- `chore` 依赖更新/脚手架配置修改等
- `workflow` 工作流改进
- `ci` 持续集成
- `types` 类型定义文件更改
- `wip` 开发中

## ☁️浏览器支持

本地开发推荐使用`Chrome 80+` 浏览器

支持现代浏览器, 不支持 IE

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt=" Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>IE | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt=" Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Chrome | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" alt="Safari" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Safari |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|                         not support                          |                       last 2 versions                        |                       last 2 versions                        |                       last 2 versions                        |                       last 2 versions                        |

## ✈️ Others

- 维护共享仓库，如有错误麻烦各位提comments ~ 
- 仓库中借鉴的内容已标明，如有未尽事宜麻烦联系 [18831786160@163.com](mailto:18831786160@163.com) ~
