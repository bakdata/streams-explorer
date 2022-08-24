import { IGroup, IShape } from "@antv/g-base";
import G6, {
  Item,
  ModelConfig,
  NodeConfig,
  ShapeOptions,
  ShapeStyle,
  UpdateType,
} from "@antv/g6";
import { deepMix } from "@antv/util";

/* Custom G6 node to display topics
 * based on builtin rectangle node
 * https://github.com/antvis/G6/blob/4.6.15/packages/element/src/nodes/rect.ts
 */

G6.registerNode(
  "TopicNode",
  {
    options: {
      style: {
        radius: 5,
        width: 22,
        height: 28,
        stroke: undefined,
        fill: "#f0f2f5",
        lineWidth: 0,
      },
      labelCfg: {
        style: {
          fill: "#000",
        },
        position: "bottom",
        offset: 10,
      },
      icon: {
        width: 36,
        height: 36,
      },
    },
    shapeType: "rect",
    drawShape(cfg?: ModelConfig, group?: IGroup): IShape {
      const style = (this as any).getShapeStyle!(cfg);
      const name = `${(this as ShapeOptions).type}-keyShape`;
      const keyShape = group!.addShape("rect", {
        attrs: style,
        className: name,
        name: name,
        draggable: true,
      });

      const options = (this as ShapeOptions).options!;
      const icon = (options as NodeConfig).icon!;
      const iconName = `${(this as ShapeOptions).type}-icon`;
      const iconImg = cfg!.node_type + ".svg";
      group!.addShape("image", {
        attrs: {
          x: -icon.width! / 2,
          y: -icon.height! / 2,
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
      const width = style.width;
      const height = style.height;
      const styles = {
        x: -width / 2,
        y: -height / 2,
        width,
        height,
        ...style,
      };

      return styles;
    },
    update(cfg: ModelConfig, item: Item, updateType?: UpdateType) {
      // update metric
      const group = item.getContainer();
      const metricLabel = group.get("children")[2];
      const metric = metricLabel.attr();
      metric.text = cfg.metric;
      metricLabel.attr(metric);

      // update other styles
      const style = { ...cfg.style };
      (this as any).updateShape(cfg, item, style, true, updateType);
    },
  },
  "single-node"
);
