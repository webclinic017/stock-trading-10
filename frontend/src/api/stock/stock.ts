import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}

/**
 * @description: 获取股票基本信息
 */
export function getStockInfo(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/stock/list',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}

/**
 * @description: 获取持仓基本信息
 */
export function getPositionInfo(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/position/list',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}

/**
 * @description: 获取股票当前市场价格
 */
export function getMarketPrice(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/stock/market_price',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}

/**
 * @description: 购买股票
 */
export function buyStock(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/position/buy',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
export function sellStock(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/position/sell',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
