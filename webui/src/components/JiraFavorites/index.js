import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import Moment from 'react-moment';
import { Spin, Icon } from 'antd';
import styles from './style.less';

@connect(({ jiraStar, loading }) => ({
  favorites: jiraStar.list,
  isLoading: loading.effects['jiraStar/getFavorites'] || false,
}))
class JiraFavorites extends React.Component {
  componentDidMount() {
    this.props.dispatch({ type: 'jiraStar/getFavorites' });
  }

  render() {
    const { favorites, isLoading } = this.props;
    return (
      <Spin spinning={isLoading}>
        {R.reverse(favorites).map(({ key, title, time }) => (
          <div className={styles.row}>
            <div>
              <a
                href={`https://jira-ext.perkinelmer.com/browse/${key}`}
                rel="noopener noreferrer"
                target="_blank"
              >
                {key}
              </a>
              : <span>{title}</span>
            </div>
            <div>
              <Icon type="clock-circle" style={{ marginRight: '4px', color: '#ccc' }} />
              starred <Moment fromNow>{time}</Moment>
            </div>
          </div>
        ))}
      </Spin>
    );
  }
}

export default JiraFavorites;
