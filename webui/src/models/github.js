import { message, notification } from 'antd';
import { getPulls, syncPulls } from '@/services/github';

export default {
  namespace: 'github',

  state: {
    repoPulls: {},
  },

  effects: {
    *getPulls({ owner, repo }, { call, put }) {
      try {
        const response = yield call(getPulls, owner, repo);
        const pulls = response.data;
        yield put({ type: 'setPulls', owner, repo, pulls });
      } catch (error) {
        message.error('Failed to fetch github pull requests');
      }
    },
    *syncPulls(_, { call }) {
      try {
        yield call(syncPulls);
        message.success('Sync github pull requests finished.');
      } catch (error) {
        message.error('Failed to sync github pull requests');
      }
    },
  },

  reducers: {
    setPulls(state, { owner, repo, pulls }) {
      const { repoPulls } = state;
      return {
        ...state,
        repoPulls: {
          ...repoPulls,
          [`${owner}/${repo}`]: pulls,
        },
      };
    },
  },
};
