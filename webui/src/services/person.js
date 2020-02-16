import request from '@/utils/request';

export async function listPersons(payload) {
  return request('/api/persons/list', {
    method: 'POST',
    body: payload,
  });
}

export async function listPhotos(personId, payload) {
  return request(`/api/persons/${personId}/photos/list`, {
    method: 'POST',
    body: payload,
  });
}

export async function renamePerson(personId, name) {
  return request(`/api/persons/${personId}/rename`, {
    method: 'POST',
    body: { name },
  });
}
