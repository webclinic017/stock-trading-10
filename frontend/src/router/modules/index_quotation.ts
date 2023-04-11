import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { BarChartOutlined } from '@vicons/antd';
import { renderIcon } from '@/utils/index';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/indexQuotation',
    name: 'IndexQuotation',
    redirect: '/indexQuotation',
    component: Layout,
    meta: {
      title: '指数行情',
      icon: renderIcon(BarChartOutlined),
      sort: 2,
    },
    children: [
      {
        path: 'index',
        name: 'index',
        meta: {
          title: '指数行情',
        },
        component: () => import('@/views/index-quotation/index.vue'),
      },
    ],
  },
];

export default routes;
