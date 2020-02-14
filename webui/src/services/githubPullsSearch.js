import request from '@/utils/request';

export async function searchPulls(payload) {
  return request('/api/github/pulls/search', {
    method: 'POST',
    body: payload,
  });
}
