import { AutoComplete, Space } from "antd";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import { Node as GraphNode } from "./api/apiSchemas";
import Node from "./graph/Node";

const ICON_SIZE = 18;

const NodeIcon = ({ nodeType }: { nodeType: string }) => (
  // eslint-disable-next-line @next/next/no-img-element
  <img
    src={nodeType + ".svg"}
    alt={nodeType + "-icon"}
    height={ICON_SIZE}
    data-testid="node-icon"
  />
);

interface SearchProps {
  nodes: GraphNode[] | undefined;
  focusedNode: Node | undefined;
  setFocusedNode: Function;
  setDetailNode: Function;
}

const Search = (props: SearchProps) => {
  const router = useRouter();
  const [width, setWidth] = useState<number>(300);

  // find longest node name and multiply string length by char width 8
  // doesn't cause long delays as builtin function
  useEffect(() => {
    if (props.nodes) {
      setWidth(Math.max(...props.nodes.map((node) => node.label.length)) * 8);
    }
  }, [props.nodes]);

  const pushRouteFocusNode = (nodeId: string) => {
    const pipeline = router.query.pipeline as string;
    router.push(
      `/?${pipeline ? `pipeline=${pipeline}&` : ""}focus-node=${nodeId}`
    );
  };

  return (
    <AutoComplete
      data-testid="node-select"
      style={{
        width: width,
        maxWidth: 480,
      }}
      placeholder="Search Node"
      allowClear={true}
      defaultActiveFirstOption={true}
      listHeight={512}
      dropdownStyle={{
        minWidth: ICON_SIZE + width,
      }}
      filterOption={(inputValue, option) =>
        option?.value.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1}
      defaultValue={props.focusedNode ? props.focusedNode.label : undefined}
      onSelect={(nodeId, option) => {
        const node = option.node as Node;
        if (node) {
          props.setFocusedNode(node);
          props.setDetailNode(node);
        }
        pushRouteFocusNode(nodeId);
      }}
    >
      {props.nodes?.map((node) => (
        <AutoComplete.Option
          data-testid="node-option"
          value={node.id}
          key={node.id}
          node={node}
        >
          <Space direction="horizontal">
            <NodeIcon nodeType={node.node_type} />
            {node.label}
          </Space>
        </AutoComplete.Option>
      ))}
    </AutoComplete>
  );
};

export default Search;
