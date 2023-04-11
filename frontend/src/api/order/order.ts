import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}
/**
 * @description: 获取订单列表
 */
export function getOrderList(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/order/list',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
