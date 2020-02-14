import React from 'react';
import { connect } from 'dva';
import { Button } from 'antd';
import GithubPullRequest from '@/components/GithubPullRequest';

@connect(({ github, loading }) => ({
  repoPulls: github.repoPulls,
  isLoading: loading.effects['github/getPulls'] || false,
}))
class GithubRepoPulls extends React.Component {
  componentDidMount() {
    this.refresh();

    const { autoRefresh } = this.props;
    if (autoRefresh > 0) {
      this.timer = window.setInterval(this.refresh, autoRefresh * 1000);
    }
  }

  componentWillUnmount() {
    window.clearInterval(this.timer);
  }

  refresh = () => {
    const { owner, repo } = this.props;
    this.props.dispatch({ type: 'github/getPulls', owner, repo });
  };

  render() {
    const { repoPulls, owner, repo } = this.props;

    const pulls = repoPulls[`${owner}/${repo}`] || [];

    return (
      <div style={{ marginTop: '8px' }}>
        <h3>
          {owner}/{repo}
          <Button icon="reload" size="small" style={{ marginLeft: '4px' }} onClick={this.refresh} />
        </h3>
        {pulls.map(pull => (
          <GithubPullRequest key={pull.url} pull={pull} />
        ))}
      </div>
    );
  }
}

export default GithubRepoPulls;
