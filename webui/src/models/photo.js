import { message } from 'antd';
import { listPhotos } from '@/services/photo';

export default {
  namespace: 'photo',

  state: {
    query: {},
    list: [],
    meta: {},
  },

  effects: {
    *listPhotos({ payload }, { call, put }) {
      try {
        const response = yield call(listPhotos, payload);
        yield put({
          type: 'setPhotos',
          query: payload,
          list: response.data,
          meta: response.meta,
        });
      } catch (error) {
        message.error('获取照片列表失败');
      }
    },
  },

  reducers: {
    setPhotos(state, { query, list, meta }) {
      return { ...state, query, list, meta };
    },
  },
};
