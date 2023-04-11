import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}
/**
 * @description: 获取龙虎榜信息
 */
export function getDtlInfo(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/dtl/list',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 获取股票日线行情
 */
export function getDailyKLine(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/quotation/daily',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 获取股票周线行情
 */
export function getWeeklyKLine(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/quotation/weekly',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 获取股票月线行情
 */
export function getMonthlyKLine(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/quotation/monthly',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
