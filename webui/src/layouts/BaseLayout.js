import React from 'react';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/es/locale/zh_CN';
import Navigator from './Navigator';
import styles from './style.less';

class BaseLayout extends React.Component {
  render() {
    const { children } = this.props;
    return (
      <ConfigProvider locale={zhCN}>
        <div className="header" />
        <div className={styles.body}>
          <Navigator />
          <div className={styles.main}>{children}</div>
        </div>
        <div className="footer" />
      </ConfigProvider>
    );
  }
}

export default BaseLayout;
