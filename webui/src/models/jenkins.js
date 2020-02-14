import { message } from 'antd';
import { getLastBuildBranches, getViewList, getJobStatus } from '@/services/jenkins';

export default {
  namespace: 'jenkins',

  state: {
    lastBuildBranches: {},
    viewList: [],
    jobStatus: [],
  },

  effects: {
    *getLastBuildBranches({ view }, { call, put }) {
      const response = yield call(getLastBuildBranches, view);
      const branches = response.data;
      yield put({ type: 'setLastBuildBranches', view, branches });
    },
    *getViewList(_, { call, put }) {
      try {
        const response = yield call(getViewList);
        yield put({ type: 'setViewList', viewList: response.data });
      } catch (error) {
        message.error('Failed to get Jenkins view list');
      }
    },
    *getJobStatus(_, { call, put }) {
      try {
        const response = yield call(getJobStatus);
        yield put({ type: 'setJobStatus', jobStatus: response.data });
      } catch (error) {
        message.error('Failed to get Jenkins job status');
      }
    },
  },

  reducers: {
    setViewList(state, { viewList }) {
      return { ...state, viewList };
    },
    setJobStatus(state, { jobStatus }) {
      return { ...state, jobStatus };
    },
    setLastBuildBranches(state, { view, branches }) {
      const { lastBuildBranches } = state;
      return {
        ...state,
        lastBuildBranches: {
          ...lastBuildBranches,
          [view]: branches,
        },
      };
    },
  },
};
