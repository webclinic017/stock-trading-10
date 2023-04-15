import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { ProfileOutlined } from '@vicons/antd';
import { renderIcon } from '@/utils/index';

/**
 * @param name 路由名称, 必须设置,且不能重名
 * @param meta 路由元信息（路由附带扩展信息）
 * @param redirect 重定向地址, 访问这个路由时,自定进行重定向
 * @param meta.disabled 禁用整个菜单
 * @param meta.title 菜单名称
 * @param meta.icon 菜单图标
 * @param meta.keepAlive 缓存该路由
 * @param meta.sort 排序越小越排前
 *
 * */
const routes: Array<RouteRecordRaw> = [
  {
    path: '/stock',
    name: 'Stock',
    redirect: '/stock',
    component: Layout,
    meta: {
      title: '股票信息',
      icon: renderIcon(ProfileOutlined),
      sort: 2,
    },
    children: [
      {
        path: 'stock-info',
        name: 'stock-info',
        meta: {
          title: '基础信息',
        },
        component: () => import('@/views/stock/stockInfo/index.vue'),
      },
      {
        path: 'company-info/:ts_code?',
        name: 'company-info',
        meta: {
          title: '公司信息',
          hidden: true,
        },
        component: () => import('@/views/stock/companyInfo/index.vue'),
      },
      {
        path: 'position',
        name: 'position',
        meta: {
          title: '持仓',
          // TODO 是否需要添加一个权限？
          // permissions: ['user-manage'],
        },
        component: () => import('@/views/stock/position/index.vue'),
      },
    ],
  },
];

export default routes;
