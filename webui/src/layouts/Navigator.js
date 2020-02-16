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

      case 'persons':
        router.push('/persons');
        break;

      default:
        break;
    }
  };

  render() {
    const currentPath = window.location.hash.substring(2);
    return (
      <Menu
        mode="inline"
        selectedKeys={[currentPath]}
        className={styles.navigator}
        onSelect={this.onSelect}
      >
        <Menu.Item key="all-photos">
          <Icon type="camera" />
          <span>所有照片</span>
        </Menu.Item>
        <Menu.Item key="persons">
          <Icon type="team" />
          <span>人物照片</span>
        </Menu.Item>
      </Menu>
    );
  }
}

export default Navigator;
