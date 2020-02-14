import React from 'react';
import { connect } from 'dva';
import { Spin, Pagination } from 'antd';
import GithubPullRequest from '@/components/GithubPullRequest';
import SearchPanel from './SearchPanel';
import TopBar from './TopBar';
import styles from './style.less';

@connect(({ githubPullsSearch, loading }) => ({
  query: githubPullsSearch.query,
  pulls: githubPullsSearch.list,
  meta: githubPullsSearch.meta,
  isLoading: loading.effects['githubPullsSearch/search'] || false,
}))
class Page extends React.Component {
  search = values => {
    this.props.dispatch({
      type: 'githubPullsSearch/search',
      payload: { ...values, pageNumber: 1, pageSize: 20 },
    });
  };

  onPageChange = (pageNumber, pageSize) => {
    const { query } = this.props;
    this.props.dispatch({
      type: 'githubPullsSearch/search',
      payload: { ...query, pageNumber, pageSize },
    });
  };

  render() {
    const { query, pulls, meta, isLoading } = this.props;
    const { pageNumber, pageSize } = query;

    return (
      <div className={styles.content}>
        <div className={styles.searchPanel}>
          <TopBar />
          <SearchPanel onSearch={this.search} />
        </div>

        <div className={styles.searchResult}>
          <Spin spinning={isLoading}>
            {pulls.map(pull => (
              <GithubPullRequest key={pull.url} pull={pull} />
            ))}
            {meta.total === 0 && <div>No result</div>}
            {meta.total > 0 && (
              <div className={styles.pager}>
                <Pagination
                  size="small"
                  showSizeChanger
                  showQuickJumper
                  current={pageNumber}
                  pageSize={pageSize}
                  total={meta.total}
                  onChange={this.onPageChange}
                  onShowSizeChange={this.onPageChange}
                  showTotal={(total, range) => `${range[0]}-${range[1]} of ${total}`}
                />
              </div>
            )}
          </Spin>
        </div>
      </div>
    );
  }
}

export default Page;
