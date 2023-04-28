import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}

/**
 * @description: 获取回测信息
 */
export function getBackTestInfo(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/backtest/info',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
