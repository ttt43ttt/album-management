import React from 'react';
import { connect } from 'dva';
import { Spin } from 'antd';
import styles from './style.less';

@connect(({ person, loading }) => ({
  query: person.query,
  persons: person.list,
  meta: person.meta,
  isLoading: loading.effects['person/listPersons'] || false,
}))
class Page extends React.Component {
  componentDidMount() {
    this.props.dispatch({ type: 'person/listPersons' });
  }

  render() {
    const { persons, isLoading } = this.props;
    return (
      <Spin spinning={isLoading}>
        <div className={styles.personGallery}>
          {persons.map(({ id, url }) => (
            <div key={id} className={styles.personCard}>
              <img alt={id} src={url} className={styles.personImage} />
              <div>{id}</div>
            </div>
          ))}
        </div>
      </Spin>
    );
  }
}

export default Page;
