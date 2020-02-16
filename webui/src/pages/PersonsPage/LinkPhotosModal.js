import React from 'react';
import { connect } from 'dva';
import { Modal, Spin } from 'antd';
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
      selectedKey: null,
    };
  }

  componentDidMount() {
    this.props.dispatch({ type: 'person/listPersons' });
  }

  render() {
    const { persons, isLoading, isSaving, personId, photoIds, onHide } = this.props;
    const { selectedKey } = this.state;

    return (
      <Modal
        visible
        title="关联照片到人物"
        onCancel={onHide}
        onOk={() => {
          this.props
            .dispatch({
              type: 'personPhoto/linkPhotosToPerson',
              payload: { photoIds, personId, newPersonId: selectedKey },
            })
            .then(onHide);
        }}
        okButtonProps={{ disabled: !selectedKey, loading: isSaving }}
      >
        <Spin spinning={isLoading}>
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
                          this.setState({ selectedKey: id });
                        } else {
                          this.setState({ selectedKey: null });
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
      </Modal>
    );
  }
}

export default LinkPhotosModal;
