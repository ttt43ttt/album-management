import { message } from 'antd';
import { searchPulls } from '@/services/githubPullsSearch';

export default {
  namespace: 'githubPullsSearch',

  state: {
    query: {},
    list: [],
    meta: {},
  },

  effects: {
    *search({ payload }, { call, put }) {
      try {
        const response = yield call(searchPulls, payload);
        yield put({
          type: 'setPulls',
          query: payload,
          list: response.data,
          meta: response.meta,
        });
      } catch (error) {
        message.error('Failed to search github pull requests');
      }
    },
  },

  reducers: {
    setPulls(state, { query, list, meta }) {
      return { ...state, query, list, meta };
    },
  },
};
