export const columns = [
  {
    title: 'id',
    key: 'user_id',
    width: 100,
  },
  {
    title: '姓名',
    key: 'name',
    width: 100,
  },
  {
    title: '性别',
    key: 'sex',
    width: 100,
    render(row) {
      return row.sex === 'male' ? '男' : '女';
    },
  },
  {
    title: '昵称',
    key: 'nick_name',
    width: 100,
  },
  {
    title: '联系方式',
    key: 'phone',
    width: 100,
  },
  {
    title: '角色',
    key: 'role',
    width: 100,
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
  },
  {
    title: '创建日期',
    key: 'create_time',
    width: 160,
  },
  {
    title: '更新日期',
    key: 'update_time',
    width: 160,
  },
];
