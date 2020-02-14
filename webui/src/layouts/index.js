import React from 'react';
import BaseLayout from './BaseLayout';

class Layout extends React.Component {
  render() {
    const { children } = this.props;
    return <BaseLayout>{children}</BaseLayout>;
  }
}

export default Layout;
