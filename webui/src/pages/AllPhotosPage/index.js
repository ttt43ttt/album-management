import React from 'react';
import { connect } from 'dva';
import { Spin, Pagination } from 'antd';
import PhotoGallery from '@/components/PhotoGallery';
import styles from './style.less';

@connect(({ photo, loading }) => ({
  query: photo.query,
  photos: photo.list,
  meta: photo.meta,
  isLoading: loading.effects['photo/listPhotos'] || false,
}))
class Page extends React.Component {
  componentDidMount() {
    this.showPhotos({});
  }

  showPhotos = values => {
    this.props.dispatch({
      type: 'photo/listPhotos',
      payload: { ...values, pageNumber: 1, pageSize: 20 },
    });
  };

  onPageChange = (pageNumber, pageSize) => {
    const { query } = this.props;
    this.props.dispatch({
      type: 'photo/listPhotos',
      payload: { ...query, pageNumber, pageSize },
    });
  };

  render() {
    const { query, photos, meta, isLoading } = this.props;
    const { pageNumber, pageSize } = query;

    return (
      <div className={styles.content}>
        <Spin spinning={isLoading}>
          <PhotoGallery photos={photos} />
          {meta.total === 0 && <div>没有发现照片</div>}
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
    );
  }
}

export default Page;
