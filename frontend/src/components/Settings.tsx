import React, { useState } from "react";
import { Modal, Button, Tooltip } from "antd";
import { SettingOutlined } from "@ant-design/icons";

const Settings = () => {
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

  return (
    <>
      <Tooltip title="Settings">
        <Button
          type="text"
          icon={<SettingOutlined style={{ fontSize: "16px", color: "#fff" }} />}
          onClick={showModal}
        />
      </Tooltip>

      {/* <Tooltip title="Settings"> */}
      {/*   <Button type="text" onClick={showModal}> */}
      {/*     <SettingOutlined style={{ fontSize: "16px", color: "#fff" }} /> */}
      {/*   </Button> */}
      {/* </Tooltip> */}

      <Modal
        title="Settings"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <p>TODO</p>
      </Modal>
    </>
  );
};

export default Settings;
