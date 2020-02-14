import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import { Card, Spin, Row, Col, Button, Tag, Icon } from 'antd';
import Moment from 'react-moment';
import moment from 'moment';
import config from '@/config';
import { useWarningIcon } from '@/utils/pageIcon';

const countUnhealthy = jobList =>
  jobList.filter(job => !R.contains(job.status, ['SUCCESS', 'RUNNING'])).length;

@connect(({ jenkins, loading }) => ({
  isLoading: loading.effects['jenkins/getJobStatus'] || false,
  jobList: jenkins.jobStatus,
}))
class JenkinsLastBuildBranch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    this.refresh();

    // refresh every 10 mins
    this.timer = window.setInterval(this.refresh, 10 * 60 * 1000);
  }

  componentDidUpdate(prevProps) {
    const hasWarning = p => countUnhealthy(p.jobList) > 0;
    if (hasWarning(prevProps) !== hasWarning(this.props)) {
      useWarningIcon('JenkinsJobStatus', hasWarning(this.props));
    }
  }

  componentWillUnmount() {
    window.clearInterval(this.timer);
  }

  refresh = () => {
    this.refreshTime = Date();
    this.props.dispatch({ type: 'jenkins/getJobStatus' });
  };

  render() {
    const { jobList, isLoading } = this.props;

    const unhealthCount = countUnhealthy(jobList);

    const statusColor = status => {
      switch (status) {
        case 'SUCCESS':
          return 'green';
        case 'FAILURE':
          return 'red';
        case 'RUNNING':
          return '#ccc';
        default:
          return 'orange';
      }
    };

    return (
      <Spin spinning={isLoading}>
        <div>
          <span>Job status</span>
          {unhealthCount > 0 && (
            <span style={{ color: 'red', marginLeft: '4px' }}>({unhealthCount} unhealthy)</span>
          )}
          <span style={{ marginLeft: '4px' }}>
            (updated&nbsp;
            <Moment fromNow>{this.refreshTime}</Moment>)
          </span>
          <Button icon="reload" size="small" style={{ marginLeft: '4px' }} onClick={this.refresh} />
        </div>
        <Row type="flex" gutter={8} style={{ margin: '8px 0 0 -4px' }}>
          {jobList
            .sort((a, b) => (a.jobName < b.jobName ? -1 : 1))
            .map(({ jobName, status, startTime, duration }) => (
              <Col sm={{ span: 4 }}>
                <Card
                  key={jobName}
                  title={
                    <a
                      target="_blank"
                      rel="noopener noreferrer"
                      href={`${config.jenkinsURL}/job/${jobName}`}
                    >
                      {jobName}
                    </a>
                  }
                >
                  <Tag color={statusColor(status)}>{status}</Tag>
                  <div>
                    <Icon type="calendar" title="Start time" style={{ marginRight: '4px' }} />
                    <Moment fromNow>{startTime}</Moment>
                  </div>
                  <div>
                    <Icon type="clock-circle" title="Run duration" style={{ marginRight: '4px' }} />
                    {moment.duration(duration).humanize()}
                  </div>
                </Card>
              </Col>
            ))}
        </Row>
      </Spin>
    );
  }
}

export default JenkinsLastBuildBranch;
