import request from '@/utils/request';

export async function getFavorites() {
  return request('/api/jira/favorites');
}
