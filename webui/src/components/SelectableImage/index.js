import React from 'react';
import classNames from 'classnames';
import styles from './style.less';

class SelectableImage extends React.Component {
  render() {
    const { src, alt, className, selected, onSelectedChange, ...restProps } = this.props;
    return (
      <img
        src={src}
        alt={alt}
        className={classNames(styles.selectable, selected && styles.active, className)}
        onClick={() => onSelectedChange(!selected)}
        {...restProps}
      />
    );
  }
}

export default SelectableImage;
