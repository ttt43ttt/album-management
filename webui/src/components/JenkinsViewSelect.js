import React from 'react';
import { connect } from 'dva';
import { Select } from 'antd';

@connect(({ jenkins, loading }) => ({
  viewList: jenkins.viewList,
  isLoading: loading.effects['jenkins/getViewList'] || false,
}))
class JenkinsViewSelect extends React.Component {
  componentDidMount() {
    this.props.dispatch({ type: 'jenkins/getViewList' });
  }

  render() {
    const { viewList, isLoading, ...restProps } = this.props;
    return (
      <Select showSearch loading={isLoading} {...restProps}>
        {viewList.map(name => (
          <Select.Option key={name} value={name}>
            {name}
          </Select.Option>
        ))}
      </Select>
    );
  }
}

export default JenkinsViewSelect;
