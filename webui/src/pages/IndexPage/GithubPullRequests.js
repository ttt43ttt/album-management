import React from 'react';
import { connect } from 'dva';
import { Spin } from 'antd';
import GithubRepoPulls from '@/components/GithubRepoPulls';

@connect(({ loading }) => ({
  isLoading: loading.effects['github/getPulls'] || false,
}))
class GithubPullRequests extends React.Component {
  render() {
    const { isLoading } = this.props;
    return (
      <Spin spinning={isLoading}>
        <GithubRepoPulls owner="PerkinElmer" repo="elements-ui2.1" autoRefresh={60 * 3} />
        <GithubRepoPulls owner="PerkinElmer" repo="elements-services" autoRefresh={60 * 10} />
      </Spin>
    );
  }
}

export default GithubPullRequests;
