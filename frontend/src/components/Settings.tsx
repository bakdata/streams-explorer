import "./Settings.css";
import React, { useState } from "react";
import { Modal, Button, Tooltip, Switch, Row, Col } from "antd";
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
          data-testid="settings-button"
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
        <Row>
          <Col flex="none">
            <div className="setting">Animate:</div>
          </Col>
          <Col flex="auto">
            <Switch
              data-testid="animate"
              checked={animate}
              onChange={onChange}
            />
          </Col>
        </Row>
      </Modal>
    </>
  );
};

export default Settings;
