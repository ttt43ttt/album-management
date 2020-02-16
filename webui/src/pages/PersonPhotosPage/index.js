import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import { Spin } from 'antd';
import PhotoGallery from '@/components/PhotoGallery';
import styles from './style.less';

@connect(({ personPhoto, loading }) => ({
  query: personPhoto.query,
  photos: personPhoto.list,
  meta: personPhoto.meta,
  isLoading: loading.effects['personPhoto/listPhotos'] || false,
}))
class Page extends React.Component {
  componentDidMount() {
    const personId = R.path(['match', 'params', 'id'], this.props);
    this.props.dispatch({ type: 'personPhoto/listPhotos', personId });
  }

  render() {
    const { photos, isLoading } = this.props;
    return (
      <Spin spinning={isLoading}>
        <PhotoGallery photos={photos} />
      </Spin>
    );
  }
}

export default Page;
