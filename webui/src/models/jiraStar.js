import { message } from 'antd';
import { getFavorites } from '@/services/jiraStar';

export default {
  namespace: 'jiraStar',

  state: {
    list: [],
  },

  effects: {
    *getFavorites(_, { call, put }) {
      try {
        const response = yield call(getFavorites);
        const list = response.data;
        yield put({ type: 'setList', list });
      } catch (error) {
        message.error('Failed to fetch Jira favorites');
      }
    },
  },

  reducers: {
    setList(state, { list }) {
      return { ...state, list };
    },
  },
};
