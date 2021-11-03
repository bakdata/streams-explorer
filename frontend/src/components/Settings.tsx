import React, { useState } from "react";
import { Modal, Button, Tooltip, Switch, Space } from "antd";
import { SettingOutlined } from "@ant-design/icons";

interface SettingsProps {
  animate: boolean;
  setAnimate: Function;
}

const Settings = ({ animate, setAnimate }: SettingsProps) => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const onChange = (checked: boolean) => {
    setAnimate(checked);
  };

  return (
    <>
      <Tooltip title="Settings">
        <Button
          type="text"
          icon={<SettingOutlined style={{ fontSize: "16px", color: "#fff" }} />}
          onClick={showModal}
        />
      </Tooltip>
      <Modal
        title="Settings"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Space direction="horizontal">
          <Switch checked={animate} onChange={onChange} />
          animate
        </Space>
      </Modal>
    </>
  );
};

export default Settings;
