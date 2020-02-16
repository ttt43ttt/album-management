import React from 'react';
import { Menu, Icon } from 'antd';
import router from '@/utils/router';
import styles from './style.less';

class Navigator extends React.Component {
  onSelect = ({ key }) => {
    switch (key) {
      case 'all-photos':
        router.push('/all-photos');
        break;

      case 'face-photos':
        router.push('/face-photos');
        break;

      default:
        break;
    }
  };

  render() {
    return (
      <Menu
        mode="inline"
        defaultSelectedKeys={[window.location.hash.substring(2)]}
        className={styles.navigator}
        onSelect={this.onSelect}
      >
        <Menu.Item key="all-photos">
          <Icon type="camera" />
          <span>所有照片</span>
        </Menu.Item>
        <Menu.Item key="face-photos">
          <Icon type="team" />
          <span>人脸照片</span>
        </Menu.Item>
      </Menu>
    );
  }
}

export default Navigator;
