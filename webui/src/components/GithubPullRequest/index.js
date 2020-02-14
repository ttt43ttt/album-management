import React from 'react';
import Moment from 'react-moment';
import { Col, Row, Tag, Icon, Badge } from 'antd';
import styles from './style.less';

class GithubPullRequest extends React.Component {
  render() {
    const { pull } = this.props;

    const {
      author,
      repo,
      number,
      title,
      url,
      bodyText,
      branch,
      baseBranch,
      updatedAt,
      requestedReviewers,
      reviewerStates,
      state = '',
    } = pull;

    const needMyReview = () =>
      ['CLOSED', 'MERGED'].indexOf(state) === -1 &&
      !!requestedReviewers.find(r => r.login === 'ttt43ttt');

    const getStatusColor = () => {
      switch (state) {
        // case 'MERGED':
        //   return '#6f42c1';

        // case 'CLOSED':
        //   return '#cb2431';

        // case 'OPEN':
        //   return '#2cbe4e';

        default:
          return needMyReview() ? '#dbab09' : '';
      }
    };

    const getStatusText = () => state.toLowerCase().replace(/(^.)/, state[0]);

    return (
      <Row key={number} type="flex" className={styles.pullRow}>
        <Col className={styles.avatar}>
          <img src={author.avatarUrl} alt={author.login} title={author.login} />
        </Col>
        <Col className={styles.titleCol}>
          <div>
            <Tag color={getStatusColor()} title={`Repo: ${repo}\nStatus: ${getStatusText()}`}>
              #{number}
            </Tag>

            <a href={url} rel="noopener noreferrer" target="_blank" title={bodyText}>
              {title}
            </a>
          </div>
          <div style={{ marginTop: '2px' }}>
            <Tag>{author.name || author.login}</Tag>

            <Tag style={{ marginRight: '2px' }} color={baseBranch === 'develop' ? '' : 'orange'}>
              {baseBranch}
            </Tag>
            <span style={{ marginRight: '2px' }}>←</span>
            <Tag>{branch}</Tag>

            <span>
              <Icon type="clock-circle" style={{ marginRight: '4px', color: '#ccc' }} />
              <span style={{ color: '#586069' }} title={updatedAt}>
                updated <Moment fromNow>{updatedAt}</Moment>
              </span>
            </span>

            <span className={styles.reviewStates}>
              {(reviewerStates || [])
                .sort((a, b) => (a.state > b.state ? -1 : 1))
                .map(({ author: reviewer, state: reviewerState }) => {
                  const statusMap = {
                    APPROVED: 'success',
                    CHANGES_REQUESTED: 'error',
                    COMMENTED: 'warning',
                  };
                  return (
                    <Badge
                      key={reviewer.login}
                      className={styles.reviewState}
                      status={statusMap[reviewerState]}
                      title={reviewerState}
                      offset={[0, 20]}
                    >
                      <img
                        className={styles.smallAvatar}
                        src={reviewer.avatarUrl}
                        alt={reviewer.login}
                        title={reviewer.name || reviewer.login}
                      />
                    </Badge>
                  );
                })}
            </span>
          </div>
        </Col>
      </Row>
    );
  }
}

export default GithubPullRequest;
