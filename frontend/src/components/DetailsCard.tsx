import React, { useRef } from "react";
import { Card } from "antd";
import { useResizeDetector } from "react-resize-detector";
import Node from "./Node";
import Details from "./Details";
import "./Details.css";

interface DetailsCardProps {
  node: Node | null;
}

const DetailsCard = ({ node }: DetailsCardProps) => {
  const ref = useRef<HTMLDivElement>(null!);
  const { width } = useResizeDetector({ targetRef: ref, handleHeight: false });
  return (
    <div ref={ref} className="details">
      <Card
        title={
          node ? `${node.label} - Details` : "Click on Node  to see Details"
        }
        bodyStyle={{}}
        style={{ width: width }}
        headStyle={{ backgroundColor: "#383838", color: "white" }}
      >
        {node ? <Details nodeID={node.id} /> : null}
      </Card>
    </div>
  );
};

export default DetailsCard;
