import { Card } from "antd";
import React, { useRef } from "react";
import { useResizeDetector } from "react-resize-detector";
import Details from "./Details";
import style from "./Details.module.css";
import Node from "./Node";

interface DetailsCardProps {
  node: Node | null;
}

const DetailsCard = ({ node }: DetailsCardProps) => {
  const ref = useRef<HTMLDivElement>(null!);
  const { width } = useResizeDetector({ targetRef: ref, handleHeight: false });
  return (
    <div ref={ref} className={style.details}>
      <Card
        title={node
          ? `${node.label} - Details`
          : "Click on Node  to see Details"}
        bodyStyle={{}}
        style={{ width: width }}
        headStyle={{ backgroundColor: "#383838", color: "white" }}
      >
        {node ? <Details nodeId={node.id} /> : null}
      </Card>
    </div>
  );
};

export default DetailsCard;
