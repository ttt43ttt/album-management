import React from 'react';
import { connect } from 'dva';
import { Spin } from 'antd';
import { Link } from 'react-router-dom';
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
          {persons.map(({ id, url, photoCount }) => (
            <div key={id} className={styles.personCard}>
              <Link to={`/persons/${id}`}>
                <img alt={id} src={url} className={styles.personImage} />
              </Link>
              <div>{photoCount}</div>
            </div>
          ))}
        </div>
      </Spin>
    );
  }
}

export default Page;
