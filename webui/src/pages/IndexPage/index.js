import React from 'react';
import { Icon } from 'antd';
import JenkinsLastBuildBranch from './JenkinsLastBuildBranch';
import JenkinsJobStatus from './JenkinsJobStatus';
import GithubPullRequests from './GithubPullRequests';

const IndexPage = () => (
  <div>
    <h2>Jenkins Jobs</h2>
    <JenkinsJobStatus />
    <JenkinsLastBuildBranch />
    <h2 style={{ marginTop: '16px' }}>
      Github Pull Requests
      <a
        target="_blank"
        href="#/github/pulls"
        title="Search Pull Requests"
        style={{ marginLeft: '8px' }}
      >
        <Icon type="search" style={{ fontSize: 'smaller' }} />
      </a>
    </h2>
    <GithubPullRequests />
  </div>
);

export default IndexPage;
