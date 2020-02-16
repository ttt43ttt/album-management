import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import { Link } from 'dva/router';
import { Spin, Button } from 'antd';
import InputToggle from '@/components/InputToggle';
import SelectableImage from '@/components/SelectableImage';
import styles from './style.less';

@connect(({ person, loading }) => ({
  query: person.query,
  persons: person.list,
  meta: person.meta,
  isLoading:
    loading.effects['person/listPersons'] ||
    loading.effects['person/mergePersons'] ||
    loading.effects['person/removePersons'] ||
    false,
}))
class Page extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedKeys: [],
    };
  }

  componentDidMount() {
    this.props.dispatch({ type: 'person/listPersons' });
  }

  render() {
    const { persons, isLoading } = this.props;
    const { selectedKeys } = this.state;
    return (
      <div>
        <div className={styles.actionBar}>
          <Button
            disabled={selectedKeys.length < 2}
            onClick={() => {
              this.props.dispatch({ type: 'person/mergePersons', ids: selectedKeys });
              this.setState({ selectedKeys: [] });
            }}
          >
            合并
          </Button>
          <Button
            disabled={selectedKeys.length < 1}
            onClick={() => {
              this.props.dispatch({ type: 'person/removePersons', ids: selectedKeys });
              this.setState({ selectedKeys: [] });
            }}
          >
            移除
          </Button>
        </div>
        <Spin spinning={isLoading}>
          <div className={styles.personGallery}>
            {persons.map(({ id, name, url, photoCount }) => {
              const isSelected = selectedKeys.indexOf(id) > -1;
              return (
                <div key={id} className={styles.personCard}>
                  <SelectableImage
                    alt={id}
                    src={url}
                    className={styles.personImage}
                    selected={isSelected}
                    onSelectedChange={selected => {
                      if (selected) {
                        this.setState({ selectedKeys: R.append(id, selectedKeys) });
                      } else {
                        this.setState({ selectedKeys: R.reject(R.equals(id), selectedKeys) });
                      }
                    }}
                  />
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
                    <div style={{ fontSize: 'smaller' }}>
                      <Link to={`/persons/${id}`}>{photoCount}张照片</Link>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </Spin>
      </div>
    );
  }
}

export default Page;
