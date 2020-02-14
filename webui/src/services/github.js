import qs from 'qs';
import request from '@/utils/request';

export async function getPulls(owner, repo) {
  const params = qs.stringify({ owner, repo });
  return request('/api/github/pulls?' + params);
}

export async function syncPulls() {
  return request('/api/github/pulls/sync', { method: 'PUT' });
}
