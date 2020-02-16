import { message } from 'antd';
import { listPersons, renamePerson, mergePersons, removePersons } from '@/services/person';

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
    *reload(_, { put, select }) {
      const { query } = yield select(state => state.person);
      yield put({ type: 'listPersons', payload: query });
    },
    *renamePerson({ personId, name }, { call, put }) {
      try {
        yield call(renamePerson, personId, name);
        yield put({ type: 'reload' });
      } catch (error) {
        message.error('修改人物名称失败');
      }
    },
    *mergePersons({ ids }, { call, put }) {
      try {
        yield call(mergePersons, ids);
        yield put({ type: 'reload' });
      } catch (error) {
        message.error('合并人物失败');
      }
    },
    *removePersons({ ids }, { call, put }) {
      try {
        yield call(removePersons, ids);
        yield put({ type: 'reload' });
      } catch (error) {
        message.error('移除人物失败');
      }
    },
  },

  reducers: {
    setPersons(state, { query, list, meta }) {
      return { ...state, query, list, meta };
    },
  },
};
