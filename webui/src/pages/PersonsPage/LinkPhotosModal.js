import React from 'react';
import { connect } from 'dva';
import { Modal, Spin, Input } from 'antd';
import SelectableImage from '@/components/SelectableImage';
import InputToggle from '@/components/InputToggle';
import styles from './style.less';

@connect(({ person, loading }) => ({
  persons: person.list,
  isLoading: loading.effects['person/listPersons'] || false,
  isSaving: loading.effects['personPhoto/linkPhotosToPerson'] || false,
}))
class LinkPhotosModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedKey: undefined,
      newPersonName: undefined,
    };
  }

  componentDidMount() {
    this.props.dispatch({ type: 'person/listPersons' });
  }

  render() {
    const { persons, isLoading, isSaving, personId, photoIds, onHide } = this.props;
    const { selectedKey, newPersonName } = this.state;

    return (
      <Modal
        visible
        title="移动照片到人物集合"
        onCancel={onHide}
        onOk={() => {
          this.props
            .dispatch({
              type: 'personPhoto/linkPhotosToPerson',
              payload: { photoIds, personId, newPersonId: selectedKey, newPersonName },
            })
            .then(onHide);
        }}
        okButtonProps={{ disabled: !(selectedKey || newPersonName), loading: isSaving }}
        width="800px"
      >
        <Spin spinning={isLoading}>
          <span>选择已有的人物集合</span>
          <div className={styles.personGallery}>
            {persons
              .filter(({ id }) => id + '' !== personId + '')
              .map(({ id, name, url, photoCount }) => {
                const isSelected = selectedKey === id;
                return (
                  <div key={id} className={styles.personCard}>
                    <SelectableImage
                      alt={id}
                      src={url}
                      className={styles.personImage}
                      selected={isSelected}
                      onSelectedChange={selected => {
                        if (selected) {
                          this.setState({ selectedKey: id, newPersonName: undefined });
                        } else {
                          this.setState({ selectedKey: undefined, newPersonName: undefined });
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
                      <div style={{ color: 'gray', fontSize: 'smaller' }}>{photoCount}张照片</div>
                    </div>
                  </div>
                );
              })}
          </div>
        </Spin>
        <div style={{ borderTop: '1px solid #eee', paddingTop: '8px' }}>
          <span>创建新的人物集合</span>
          <Input
            value={newPersonName}
            placeholder="请输入人名"
            onChange={e => {
              this.setState({ selectedKey: undefined, newPersonName: e.target.value });
            }}
          />
        </div>
      </Modal>
    );
  }
}

export default LinkPhotosModal;
