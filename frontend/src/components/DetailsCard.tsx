import React, { useRef } from "react";
import { Card } from "antd";
import useDimensions from "react-cool-dimensions";
import Details from "./Details";
import "./Details.css";

interface DetailsCardProps {
  nodeID: string | null;
}

const DetailsCard = ({ nodeID }: DetailsCardProps) => {
  const ref = useRef<HTMLDivElement>(null!);
  const { width } = useDimensions({ ref });
  return (
    <div ref={ref} className="details">
      <Card
        title={nodeID ? `${nodeID} - Details` : "Click on Node  to see Details"}
        bodyStyle={{}}
        style={{ width: width }}
        headStyle={{ backgroundColor: "#4a4e4d", color: "white" }}
      >
        {nodeID ? <Details nodeID={nodeID} /> : null}
      </Card>
    </div>
  );
};

export default DetailsCard;
