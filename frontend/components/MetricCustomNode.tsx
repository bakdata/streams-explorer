import { IGroup, IShape } from "@antv/g-base";
import {
  Item,
  ModelConfig,
  NodeConfig,
  registerNode,
  ShapeStyle,
  UpdateType,
} from "@antv/g6-core";
import { deepMix } from "@antv/util";

/* Custom G6 node to display metrics
 * based on builtin circle node
 * https://github.com/antvis/G6/blob/master/packages/element/src/nodes/circle.ts
 */

registerNode(
  "MetricCustomNode",
  {
    options: {
      style: {
        x: 0,
        y: 0,
        stroke: undefined,
        fill: "#F0F2F5",
        lineWidth: 0,
      },
      labelCfg: {
        style: {
          fill: "#000000",
          fontSize: 14,
        },
        position: "bottom",
      },
      icon: {
        width: 36,
        height: 36,
      },
    },
    shapeType: "circle",
    labelPosition: "center",
    drawShape(cfg?: ModelConfig, group?: IGroup): IShape {
      const style = (this as any).getShapeStyle!(cfg);
      const name = `${(this as any).type}-keyShape`;
      const keyShape: IShape = group!.addShape("circle", {
        attrs: style,
        className: name,
        name,
        draggable: true,
      });

      const icon = (this as any).options.icon;
      const iconName = `${(this as any).type}-icon`;
      const iconImg = cfg!.node_type + ".svg";
      group!.addShape("image", {
        attrs: {
          x: -icon.width / 2,
          y: -icon.height / 2,
          img: iconImg,
          ...icon,
        },
        className: iconName,
        name: iconName,
        draggable: true,
      });

      // metrics text
      group!.addShape("text", {
        attrs: {
          textBaseline: "top",
          y: 38,
          lineHeight: 20,
          text: "",
          fill: "#333",
          fontStyle: "italic",
          textAlign: "center",
        },
        name: "metric",
      });

      return keyShape;
    },
    getShapeStyle(cfg: NodeConfig): ShapeStyle {
      const { style: defaultStyle } = (this as any).getOptions(
        cfg
      ) as NodeConfig;
      const strokeStyle = {
        stroke: cfg.color,
      };
      const style = deepMix({}, defaultStyle, strokeStyle);
      const styles = {
        x: 0,
        y: 0,
        r: 14,
        ...style,
      };
      return styles;
    },
    update(cfg: ModelConfig, item: Item, updateType?: UpdateType) {
      const group = item.getContainer();
      const metricLabel = group.get("children")[2]; // get shape containing our metric label
      const metric = metricLabel.attr();
      metric.text = cfg.metric;
      metricLabel.attr(metric); // update metric label

      // update other styles
      const style = { ...cfg.style };
      (this as any).updateShape(cfg, item, style, true, updateType);
    },
  },
  "single-node"
);
