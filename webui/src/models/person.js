import { message } from 'antd';
import { listPersons } from '@/services/person';

export default {
  namespace: 'person',

  state: {
    query: {},
    list: [],
    meta: {},
  },

  effects: {
    *listPersons({ payload }, { call, put }) {
      try {
        const response = yield call(listPersons, payload);
        yield put({
          type: 'setPersons',
          query: payload,
          list: response.data,
          meta: response.meta,
        });
      } catch (error) {
        message.error('获取人物列表失败');
      }
    },
  },

  reducers: {
    setPersons(state, { query, list, meta }) {
      return { ...state, query, list, meta };
    },
  },
};
