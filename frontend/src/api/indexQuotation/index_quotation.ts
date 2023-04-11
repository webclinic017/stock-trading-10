import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}
/**
 * @description: 获取指数日线行情
 */
export function getDailyKLine(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/indexQuotation/index_daily',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 获取指数周线行情
 */
export function getWeeklyKLine(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/indexQuotation/index_weekly',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 获取指数月线行情
 */
export function getMonthlyKLine(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/indexQuotation/index_monthly',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
