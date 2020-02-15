import request from '@/utils/request';

export async function listPhotos(payload) {
  return request('/api/photos/list', {
    method: 'POST',
    body: payload,
  });
}
