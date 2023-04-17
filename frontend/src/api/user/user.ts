import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}

/**
 * @description: 获取用户信息
 */
export function getUserInfo() {
  return http.request({
    url: '/v1/user/info',
    method: 'get',
  });
}

/**
 * @description: 用户修改个人信息
 */
export function updateUserInfo(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/update',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}

/**
 * @description: 用户登录
 */
export function login(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/login',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 用户登出
 */
export function logout(params) {
  return http.request({
    url: '/login/logout',
    method: 'POST',
    params,
  });
}
/**
 * @description: 获取用户列表
 */
export function getList(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/list',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 修改用户信息
 */
export function editUser(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/edit',
      method: 'PUT',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 新增用户
 */
export function addUser(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/add',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 删除用户
 */
export function deleteUser(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/delete',
      method: 'DELETE',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
/**
 * @description: 用户注册
 */
export function userRegister(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/v1/user/register',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}
