import { SettingOutlined } from "@ant-design/icons";
import { Button, Col, Modal, Row, Switch, Tooltip } from "antd";
import React, { useEffect, useState } from "react";
import { useVersionApiVersionGet } from "./api/fetchers";
import style from "./Settings.module.css";

const ANIMATE = "animate";

interface SettingsProps {
  animate: boolean;
  setAnimate: Function;
}

const Settings = ({ animate, setAnimate }: SettingsProps) => {
  const [visible, setVisible] = useState(false);
  const { data: version } = useVersionApiVersionGet({});

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
        centered
        visible={visible}
        footer={<p className={style.version}>Streams Explorer {version}</p>}
        onCancel={() => setVisible(false)}
      >
        <Row>
          <Col flex="none">
            <div className={style.setting}>Animate data flow:</div>
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
