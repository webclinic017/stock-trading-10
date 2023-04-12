import { http } from '@/utils/http/axios';
import { BasicResponseModel } from '@/api/stock/stock';

/**
 * @description: 获取账户基本信息用于主页展示
 */
export function getAccount() {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/account/all',
      method: 'POST',
    },
    {
      isTransformResponse: false,
    }
  );
}
export function getPosition() {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/position/all',
      method: 'POST',
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 获取订单基本信息用于主页展示
 */
export function getOrder() {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/order/all',
      method: 'POST',
    },
    {
      isTransformResponse: false,
    }
  );
}
