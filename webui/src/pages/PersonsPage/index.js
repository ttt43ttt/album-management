import React from 'react';
import { connect } from 'dva';
import { Link } from 'dva/router';
import { Spin } from 'antd';
import InputToggle from '@/components/InputToggle';
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
          {persons.map(({ id, name, url, photoCount }) => (
            <div key={id} className={styles.personCard}>
              <Link to={`/persons/${id}`}>
                <img alt={id} src={url} className={styles.personImage} />
              </Link>
              <div>
                <div>
                  <InputToggle
                    value={name}
                    placeholder="设置名字"
                    onChange={newName =>
                      this.props.dispatch({
                        type: 'person/renamePerson',
                        personId: id,
                        name: newName,
                      })
                    }
                  />
                </div>
                <div style={{ color: 'gray', fontSize: 'smaller' }}>{photoCount}张照片</div>
              </div>
            </div>
          ))}
        </div>
      </Spin>
    );
  }
}

export default Page;
