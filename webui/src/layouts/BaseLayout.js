import React from 'react';

class BaseLayout extends React.Component {
  render() {
    const { children } = this.props;
    return (
      <>
        <div className="header" />
        {children}
        <div className="footer" />
      </>
    );
  }
}

export default BaseLayout;
