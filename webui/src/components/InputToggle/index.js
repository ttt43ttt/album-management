import React from 'react';
import { Input, Button } from 'antd';
import styles from './style.less';

class InputToggle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      editing: false,
    };
    this.inputRef = React.createRef();
  }

  saveValue = () => {
    const newValue = this.inputRef.current.input.value;
    this.props.onChange(newValue);
    this.setState({ editing: false });
  };

  render() {
    const { value, placeholder } = this.props;
    const { editing } = this.state;
    if (editing) {
      return (
        <span>
          <Input ref={this.inputRef} defaultValue={value} autoFocus onPressEnter={this.saveValue} />
          <div className={styles.buttons}>
            <Button type="primary" onClick={this.saveValue}>
              保存
            </Button>
            <Button onClick={() => this.setState({ editing: false })}>取消</Button>
          </div>
        </span>
      );
    }
    return <span onClick={() => this.setState({ editing: !editing })}>{value || placeholder}</span>;
  }
}

export default InputToggle;
