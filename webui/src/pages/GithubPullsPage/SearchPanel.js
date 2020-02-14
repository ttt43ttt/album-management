import React from 'react';
import { Select, Button, Form, Row, DatePicker, Input } from 'antd';
import moment from 'moment';
import styles from './style.less';

const { RangePicker } = DatePicker;

const formItemLayout = {
  // labelCol: {
  //   xs: { span: 24 },
  //   sm: { span: 6 },
  // },
  // wrapperCol: {
  //   xs: { span: 24 },
  //   sm: { span: 18 },
  // },
};

const stateList = ['OPEN', 'MERGED', 'CLOSED'];

const reviewStateList = ['APPROVED', 'COMMENTED', 'CHANGES_REQUESTED'];

const repoList = ['elements-ui2.1', 'Elements-Services', 'annotation-editor'];

const userList = [
  'Wilson Tian',
  'Xing Gao',
  'Leeloo Zhang',
  'James Sun',
  'Seven Jin',
  'Shawn Zou',
  'Frank Zhou',
  'Liu, Xue-zhe(Boris)',
];

const reviewerList = ['Wilson Tian', 'Michael Plotke', 'Eddie Joo'];

class SearchPanel extends React.Component {
  componentDidMount() {
    this.search();
  }

  search = () => {
    const { form, onSearch } = this.props;
    form.validateFields((err, values) => {
      if (!err) {
        onSearch(values);
      }
    });
  };

  render() {
    const { form } = this.props;

    const setRecentDays = n => {
      const from = moment().subtract(n, 'days');
      const to = moment();
      form.setFieldsValue({ updatedAt: [from, to] });
    };

    return (
      <Form {...formItemLayout}>
        <Form.Item label="Repo">
          {form.getFieldDecorator('repo', { initialValue: [] })(
            <Select placeholder="Select repos" mode="tags" allowClear>
              {repoList.map(value => (
                <Select.Option key={value} value={value}>
                  {value}
                </Select.Option>
              ))}
            </Select>
          )}
        </Form.Item>

        <Form.Item label="Author">
          {form.getFieldDecorator('author', { initialValue: [] })(
            <Select placeholder="Select author" mode="tags" allowClear>
              {userList.map(value => (
                <Select.Option key={value} value={value}>
                  {value}
                </Select.Option>
              ))}
            </Select>
          )}
        </Form.Item>

        <Form.Item label="Title or Description">
          {form.getFieldDecorator('title', { initialValue: '' })(
            <Input placeholder="Search title or description" allowClear />
          )}
        </Form.Item>

        <Form.Item label="Base Branch">
          {form.getFieldDecorator('baseBranch', { initialValue: '' })(
            <Input placeholder="Base branch" allowClear />
          )}
        </Form.Item>

        <Form.Item label="Reviewed By">
          {form.getFieldDecorator('reviewer', { initialValue: [] })(
            <Select placeholder="Select reviewer" mode="tags" allowClear>
              {reviewerList.map(value => (
                <Select.Option key={value} value={value}>
                  {value}
                </Select.Option>
              ))}
            </Select>
          )}
        </Form.Item>

        <Form.Item label="Review State">
          {form.getFieldDecorator('reviewState', { initialValue: [] })(
            <Select placeholder="Select review state" mode="tags" allowClear>
              {reviewStateList.map(value => (
                <Select.Option key={value} value={value}>
                  {value}
                </Select.Option>
              ))}
            </Select>
          )}
        </Form.Item>

        <Form.Item label="State">
          {form.getFieldDecorator('state', { initialValue: ['MERGED'] })(
            <Select placeholder="Select states" mode="tags" allowClear>
              {stateList.map(value => (
                <Select.Option key={value} value={value}>
                  {value}
                </Select.Option>
              ))}
            </Select>
          )}
        </Form.Item>

        <Form.Item label="Updated At">
          {form.getFieldDecorator('updatedAt', {
            initialValue: [moment().subtract(1, 'year'), moment()],
          })(
            <RangePicker
              format="YYYY-MM-DD"
              showTime={{
                defaultValue: [moment('00:00:00', 'HH:mm:ss'), moment('11:59:59', 'HH:mm:ss')],
              }}
              style={{ width: '100%' }}
            />
          )}
          <div className={styles.days}>
            <a onClick={() => setRecentDays(1)}>recent 1 day</a>
            <a onClick={() => setRecentDays(7)}>recent 1 week</a>
            <a onClick={() => setRecentDays(30)}>recent 1 month</a>
          </div>
        </Form.Item>

        <Form.Item label="Sort">
          {form.getFieldDecorator('sort', { initialValue: 'closedAt-desc' })(
            <Select>
              <Select.Option value="closedAt-desc">Recently closed</Select.Option>
              <Select.Option value="updatedAt-desc">Recently updated</Select.Option>
              <Select.Option value="updatedAt-asc">Least recently updated</Select.Option>
              <Select.Option value="createdAt-desc">Newest created</Select.Option>
              <Select.Option value="createdAt-asc">Oldest created</Select.Option>
            </Select>
          )}
        </Form.Item>

        <Row>
          <Button type="primary" onClick={this.search}>
            Search
          </Button>
        </Row>
      </Form>
    );
  }
}

export default Form.create()(SearchPanel);
