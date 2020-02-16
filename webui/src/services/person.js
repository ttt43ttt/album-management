import request from '@/utils/request';

export async function listPersons(payload) {
  return request('/api/persons/list', {
    method: 'POST',
    body: payload,
  });
}
