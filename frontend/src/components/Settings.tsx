import "./Settings.css";
import React, { useState, useEffect } from "react";
import { Modal, Button, Tooltip, Switch, Row, Col } from "antd";
import { SettingOutlined } from "@ant-design/icons";

const ANIMATE = "animate";

interface SettingsProps {
  animate: boolean;
  setAnimate: Function;
}

const Settings = ({ animate, setAnimate }: SettingsProps) => {
  const [visible, setVisible] = useState(false);

  // on initial page load
  useEffect(() => {
    const storedAnimate = localStorage.getItem(ANIMATE);
    if (storedAnimate) setAnimate(storedAnimate === "true");
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // save state to local storage
  useEffect(() => {
    localStorage.setItem(ANIMATE, animate.toString());
  }, [animate]);

  const onChange = (checked: boolean) => setAnimate(checked);

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
            <div className="setting">Animate graph activity:</div>
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
