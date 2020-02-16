import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import { Button, Spin, Pagination } from 'antd';
import PhotoGallery from '@/components/PhotoGallery';
import LinkPhotosModal from '@/pages/PersonsPage/LinkPhotosModal';
import styles from './style.less';

@connect(({ personPhoto, loading }) => ({
  query: personPhoto.query,
  photos: personPhoto.list,
  meta: personPhoto.meta,
  isLoading: loading.effects['personPhoto/listPhotos'] || false,
}))
class Page extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedKeys: [],
      linkPhotosModal: { visible: false },
    };
  }

  componentDidMount() {
    this.props.dispatch({
      type: 'personPhoto/listPhotos',
      personId: this.getPersonId(),
      payload: { pageNumber: 1, pageSize: 20 },
    });
  }

  getPersonId = () => R.path(['match', 'params', 'id'], this.props);

  onPageChange = (pageNumber, pageSize) => {
    const { query } = this.props;
    this.props.dispatch({
      type: 'personPhoto/listPhotos',
      personId: this.getPersonId(),
      payload: { ...query, pageNumber, pageSize },
    });
  };

  render() {
    const { query, photos, meta, isLoading } = this.props;
    const { selectedKeys, linkPhotosModal } = this.state;
    const { pageNumber, pageSize } = query;

    return (
      <div>
        <div className={styles.actionBar}>
          <Button
            disabled={selectedKeys.length < 1}
            onClick={() => {
              this.setState({
                linkPhotosModal: {
                  visible: true,
                  personId: this.getPersonId(),
                  photoIds: selectedKeys,
                },
              });
            }}
          >
            不是此人...
          </Button>
        </div>
        <Spin spinning={isLoading}>
          <PhotoGallery
            photos={photos}
            selectable
            selectedKeys={selectedKeys}
            onSelectedChange={selected => this.setState({ selectedKeys: selected })}
          />
          {meta.total === 0 && <div>没有找到此人的照片</div>}
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
        {linkPhotosModal.visible && (
          <LinkPhotosModal
            {...linkPhotosModal}
            onHide={() => this.setState({ linkPhotosModal: { visible: false } })}
          />
        )}
      </div>
    );
  }
}

export default Page;
