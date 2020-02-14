import React from 'react';
import { connect } from 'dva';
import { Icon, Menu, Dropdown } from 'antd';
import styles from './style.less';

@connect(() => ({}))
class TopBar extends React.Component {
  handleClick = ({ key }) => {
    switch (key) {
      case 'export':
        window.open('/api/github/pulls/export/pull_requests.csv');
        break;

      case 'sync':
        this.props.dispatch({ type: 'github/syncPulls' });
        break;

      default:
        break;
    }
  };

  render() {
    const menu = (
      <Menu onClick={this.handleClick}>
        <Menu.Item key="sync">Sync Pull Requests</Menu.Item>
        <Menu.Item key="export">Export to .csv</Menu.Item>
      </Menu>
    );

    return (
      <div className={styles.topbar}>
        <Dropdown overlay={menu} trigger={['click']} placement="bottomRight">
          <Icon type="menu" />
        </Dropdown>
      </div>
    );
  }
}

export default TopBar;
