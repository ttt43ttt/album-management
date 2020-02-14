import qs from 'qs';
import request from '@/utils/request';

export async function getLastBuildBranches(viewName) {
  const params = qs.stringify({ view: viewName });
  return request('/api/jenkins/last-build-branches?' + params);
}

export async function getViewList() {
  return request('/api/jenkins/views');
}

export async function getJobStatus() {
  return request('/api/jenkins/job-status');
}
