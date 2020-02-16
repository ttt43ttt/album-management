import React from 'react';
import * as R from 'ramda';
import SelectableImage from '@/components/SelectableImage';
import styles from './style.less';

class PhotoGallery extends React.Component {
  render() {
    const { photos, selectable, selectedKeys, onSelectedChange } = this.props;
    return (
      <div className={styles.photoGallery}>
        {photos.map(({ id, url }) => (
          <div key={id} className={styles.photoContainer}>
            {selectable && (
              <SelectableImage
                alt={url}
                src={url}
                className={styles.photo}
                selected={selectedKeys.indexOf(id) > -1}
                onSelectedChange={isSelected => {
                  const newSelected = isSelected
                    ? R.append(id, selectedKeys)
                    : R.reject(R.equals(id), selectedKeys);
                  onSelectedChange(newSelected);
                }}
              />
            )}
            {!selectable && <img alt={url} src={url} className={styles.photo} />}
          </div>
        ))}
      </div>
    );
  }
}

export default PhotoGallery;
