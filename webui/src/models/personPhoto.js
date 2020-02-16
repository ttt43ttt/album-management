import { message } from 'antd';
import { listPhotos } from '@/services/person';

export default {
  namespace: 'personPhoto',

  state: {
    query: {},
    list: [],
    meta: {},
  },

  effects: {
    *listPhotos({ personId, payload }, { call, put }) {
      try {
        const response = yield call(listPhotos, personId, payload);
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
