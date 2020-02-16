import React from 'react';
import * as R from 'ramda';
import { connect } from 'dva';
import { Button, Spin, Pagination, Menu, Dropdown, Icon } from 'antd';
import PhotoGallery from '@/components/PhotoGallery';
import InputToggle from '@/components/InputToggle';
import LinkPhotosModal from '@/pages/PersonsPage/LinkPhotosModal';
import styles from './style.less';

@connect(({ person, personPhoto, loading }) => ({
  persons: person.list,
  query: personPhoto.query,
  photos: personPhoto.list,
  meta: personPhoto.meta,
  isLoading: loading.effects['personPhoto/listPhotos'] || false,
}))
class Page extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedKeys: [],
      linkPhotosModal: { visible: false },
    };
  }

  componentDidMount() {
    if (this.props.persons.length === 0) {
      this.props.dispatch({ type: 'person/listPersons' });
    }

    this.props.dispatch({
      type: 'personPhoto/listPhotos',
      personId: this.getPersonId(),
      payload: { pageNumber: 1, pageSize: 20 },
    });
  }

  getPersonId = () => {
    const id = R.path(['match', 'params', 'id'], this.props);
    return Number(id);
  };

  onPageChange = (pageNumber, pageSize) => {
    const { query } = this.props;
    this.props.dispatch({
      type: 'personPhoto/listPhotos',
      personId: this.getPersonId(),
      payload: { ...query, pageNumber, pageSize },
    });
  };

  render() {
    const { persons, query, photos, meta, isLoading } = this.props;
    const { selectedKeys, linkPhotosModal } = this.state;
    const { pageNumber, pageSize } = query;
    const personId = this.getPersonId();

    const menu = (
      <Menu
        onClick={({ key }) => {
          switch (key) {
            case 'remove':
              this.props.dispatch({
                type: 'personPhoto/linkPhotosToPerson',
                payload: { photoIds: selectedKeys, personId, newPersonId: null },
              });
              break;

            case 'linkToOthers':
              this.setState({
                linkPhotosModal: { visible: true, personId, photoIds: selectedKeys },
              });
              break;
            default:
              break;
          }
        }}
      >
        <Menu.Item key="linkToOthers">移动到他人集合...</Menu.Item>
        <Menu.Item key="remove">从此人集合中移除</Menu.Item>
      </Menu>
    );

    const person = R.find(p => p.id === personId, persons);

    return (
      <div>
        <div className={styles.actionBar}>
          {person && (
            <div className={styles.personInfo}>
              <div>
                <InputToggle
                  value={person.name}
                  placeholder="设置名字"
                  onChange={newName =>
                    this.props.dispatch({
                      type: 'person/renamePerson',
                      personId: person.id,
                      name: newName,
                    })
                  }
                />
              </div>
              <div style={{ color: 'gray', fontSize: 'smaller' }}>{person.photoCount}张照片</div>
            </div>
          )}

          <Dropdown overlay={menu} disabled={selectedKeys.length < 1}>
            <Button>
              不是此人 <Icon type="down" />
            </Button>
          </Dropdown>
        </div>

        <Spin spinning={isLoading}>
          <PhotoGallery
            photos={photos}
            selectable
            selectedKeys={selectedKeys}
            onSelectedChange={selected => this.setState({ selectedKeys: selected })}
          />
          {meta.total === 0 && <div>没有找到此人的照片</div>}
          {meta.total > 0 && (
            <div className={styles.pager}>
              <Pagination
                size="small"
                showSizeChanger
                showQuickJumper
                current={pageNumber}
                pageSize={pageSize}
                total={meta.total}
                onChange={this.onPageChange}
                onShowSizeChange={this.onPageChange}
                showTotal={(total, range) => `${range[0]}-${range[1]} of ${total}`}
              />
            </div>
          )}
        </Spin>
        {linkPhotosModal.visible && (
          <LinkPhotosModal
            {...linkPhotosModal}
            onHide={() => this.setState({ linkPhotosModal: { visible: false } })}
          />
        )}
      </div>
    );
  }
}

export default Page;
