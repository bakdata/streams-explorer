import React, { useRef } from "react";
import { Card, Space } from "antd";
import { useResizeDetector } from "react-resize-detector";
import Details from "./Details";
import Schema from "./Schema";
import "./Details.css";

interface DetailsCardProps {
  nodeID: string | null;
}

const DetailsCard = ({ nodeID }: DetailsCardProps) => {
  const ref = useRef<HTMLDivElement>(null!);
  const { width } = useResizeDetector({ targetRef: ref, handleHeight: false });
  return (
    <div ref={ref} className="details">
      <Card
        title={nodeID ? `${nodeID} - Details` : "Click on Node  to see Details"}
        bodyStyle={{}}
        style={{ width: width }}
        headStyle={{ backgroundColor: "#383838", color: "white" }}
      >
        {nodeID ? (
          <Space className="details" direction="vertical">
            <Details nodeID={nodeID} />
            <Schema nodeID={nodeID} />
          </Space>
        ) : null}
      </Card>
    </div>
  );
};

export default DetailsCard;
