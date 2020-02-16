import React from 'react';
import styles from './style.less';

class PhotoGallery extends React.Component {
  render() {
    const { photos } = this.props;
    return (
      <div className={styles.photoGallery}>
        {photos.map(({ id, url }) => (
          <div key={id} className={styles.photoContainer}>
            <img alt={url} src={url} className={styles.photo} />
          </div>
        ))}
      </div>
    );
  }
}

export default PhotoGallery;
