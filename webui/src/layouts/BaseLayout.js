import React from 'react';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/es/locale/zh_CN';

class BaseLayout extends React.Component {
  render() {
    const { children } = this.props;
    return (
      <ConfigProvider locale={zhCN}>
        <div className="header" />
        {children}
        <div className="footer" />
      </ConfigProvider>
    );
  }
}

export default BaseLayout;
