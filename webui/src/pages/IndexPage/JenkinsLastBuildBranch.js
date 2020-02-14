import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import { Card, Button, Tree, Row, Col } from 'antd';
import JenkinsViewSelect from '@/components/JenkinsViewSelect';

@connect(({ jenkins, loading }) => ({
  isLoading: loading.effects['jenkins/getLastBuildBranches'] || false,
  lastBuildBranches: jenkins.lastBuildBranches,
}))
class JenkinsLastBuildBranch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      view: 'snb-dev-build',
    };
  }

  render() {
    const { lastBuildBranches, isLoading } = this.props;
    const { view } = this.state;

    const branchesMap = lastBuildBranches[view] || {};
    const treeData = R.keys(branchesMap).map(branch => {
      const jobs = branchesMap[branch];
      return {
        key: branch,
        title: (
          <span>
            <span>{branch}</span>
            <span>({jobs.length})</span>
          </span>
        ),
        children: jobs.map(job => ({ key: job, title: job })),
      };
    });

    return (
      <Card title="Last build branches" style={{ marginTop: '8px' }}>
        <Row gutter={8}>
          <Col sm={{ span: 20 }}>
            <JenkinsViewSelect
              placeholder="Select a view"
              style={{ width: '100%' }}
              value={view}
              onChange={value => this.setState({ view: value })}
            />
          </Col>
          <Col sm={{ span: 4 }}>
            <Button
              loading={isLoading}
              onClick={() => this.props.dispatch({ type: 'jenkins/getLastBuildBranches', view })}
            >
              Load
            </Button>
          </Col>
        </Row>
        <Tree treeData={treeData} />
      </Card>
    );
  }
}

export default JenkinsLastBuildBranch;
