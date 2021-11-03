import React, { useState } from "react";
import { Modal, Button, Tooltip, Switch, Space } from "antd";
import { SettingOutlined } from "@ant-design/icons";

interface SettingsProps {
  animate: boolean;
  setAnimate: Function;
}

const Settings = ({ animate, setAnimate }: SettingsProps) => {
  const [visible, setVisible] = useState(false);

  const onChange = (checked: boolean) => {
    setAnimate(checked);
  };

  return (
    <>
      <Tooltip title="Settings">
        <Button
          type="text"
          icon={<SettingOutlined style={{ fontSize: "16px", color: "#fff" }} />}
          onClick={() => setVisible(true)}
        />
      </Tooltip>
      <Modal
        title="Settings"
        visible={visible}
        footer={null}
        onCancel={() => setVisible(false)}
      >
        <Space direction="horizontal">
          Animate:
          <Switch checked={animate} onChange={onChange} />
        </Space>
      </Modal>
    </>
  );
};

export default Settings;
