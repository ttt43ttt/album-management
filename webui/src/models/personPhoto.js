import { message } from 'antd';
import { listPhotos, linkPhotosToPerson } from '@/services/person';

export default {
  namespace: 'personPhoto',

  state: {
    personId: null,
    query: {},
    list: [],
    meta: {},
  },

  effects: {
    *listPhotos({ personId, payload }, { call, put }) {
      try {
        const response = yield call(listPhotos, personId, payload);
        yield put({
          type: 'setPersonPhotos',
          personId,
          query: payload,
          list: response.data,
          meta: response.meta,
        });
      } catch (error) {
        message.error('获取人物列表失败');
      }
    },
    *reload(_, { put, select }) {
      const { personId, query } = yield select(state => state.personPhoto);
      yield put({ type: 'listPhotos', personId, payload: query });
    },
    *linkPhotosToPerson({ payload }, { call, put }) {
      try {
        yield call(linkPhotosToPerson, payload);
        yield put({ type: 'reload' });
      } catch (error) {
        message.error('关联人物照片失败');
      }
    },
  },

  reducers: {
    setPersonPhotos(state, { personId, query, list, meta }) {
      return { ...state, personId, query, list, meta };
    },
  },
};
