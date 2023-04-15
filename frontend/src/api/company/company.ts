import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}

/**
 * @description: 获取公司信息
 */
export function getCompanyInfo(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/company/info',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
