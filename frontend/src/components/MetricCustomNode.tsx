import G6, {
  Global,
  Item,
  ModelConfig,
  NodeConfig,
  ShapeOptions,
  ShapeStyle,
} from "@antv/g6";
import GGroup from "@antv/g-canvas/lib/group";
import { IGroup, IShape } from "@antv/g-canvas/lib/interfaces";
import deepMix from "@antv/util/lib/deep-mix";

G6.registerNode(
  "MetricCustomNode",
  {
    options: {
      size: Global.defaultNode.size,
      style: {
        x: 0,
        y: 0,
        stroke: Global.defaultNode.style.stroke,
        fill: Global.defaultNode.style.fill,
        lineWidth: Global.defaultNode.style.lineWidth,
      },
      labelCfg: {
        style: {
          fill: "#595959",
        },
      },
      linkPoints: {
        top: false,
        right: false,
        bottom: false,
        left: false,
        size: 10,
        lineWidth: 1,
        fill: "#72CC4A",
        stroke: "#72CC4A",
      },
      icon: {
        show: false,
        img: "",
        width: 16,
        height: 16,
      },
    },
    shapeType: "circle",
    labelPosition: "center",
    drawShape(cfg: ModelConfig | undefined, group: IGroup | undefined): IShape {
      const { icon: defaultIcon = {} } = (this as any).getOptions(
        cfg
      ) as NodeConfig;
      const style = (this as any).getShapeStyle!(cfg);
      const icon = deepMix({}, defaultIcon, cfg!.icon);
      const keyShape: IShape = group!.addShape("circle", {
        attrs: style,
        className: `${(this as any).type}-keyShape`,
        draggable: true,
      });

      const { width, height, show } = icon;
      if (show) {
        group!.addShape("image", {
          attrs: {
            x: -width / 2,
            y: -height / 2,
            ...icon,
          },
          className: `${(this as any).type}-icon`,
          name: `${(this as any).type}-icon`,
          draggable: true,
        });
      }

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

      (this as any).drawLinkPoints(cfg, group);

      return keyShape;
    },
    drawLinkPoints(cfg: NodeConfig, group: GGroup) {
      const { linkPoints = {} } = (this as any).getOptions(cfg) as NodeConfig;

      const {
        top,
        left,
        right,
        bottom,
        size: markSize,
        r: markR,
        ...markStyle
      } = linkPoints;
      const size = (this as any).getSize!(cfg);
      const r = size[0] / 2;
      if (left) {
        // left circle
        group.addShape("circle", {
          attrs: {
            ...markStyle,
            x: -r,
            y: 0,
            r: (this as any).markSize / 2 || markR || 5,
          },
          className: "link-point-left",
          name: "link-point-left",
          isAnchorPoint: true,
        });
      }

      if (right) {
        // right circle
        group.addShape("circle", {
          attrs: {
            ...markStyle,
            x: r,
            y: 0,
            r: (this as any).markSize / 2 || markR || 5,
          },
          className: "link-point-right",
          name: "link-point-right",
          isAnchorPoint: true,
        });
      }

      if (top) {
        // top circle
        group.addShape("circle", {
          attrs: {
            ...markStyle,
            x: 0,
            y: -r,
            r: (this as any).markSize / 2 || markR || 5,
          },
          className: "link-point-top",
          name: "link-point-top",
          isAnchorPoint: true,
        });
      }

      if (bottom) {
        // bottom circle
        group.addShape("circle", {
          attrs: {
            ...markStyle,
            x: 0,
            y: r,
            r: (this as any).markSize / 2 || markR || 5,
          },
          className: "link-point-bottom",
          name: "link-point-bottom",
          isAnchorPoint: true,
        });
      }
    },
    getShapeStyle(cfg: NodeConfig): ShapeStyle {
      const { style: defaultStyle } = (this as any).getOptions(
        cfg
      ) as NodeConfig;
      const strokeStyle = {
        stroke: cfg.color,
      };
      const style = deepMix({}, defaultStyle, strokeStyle);
      const size = (this as ShapeOptions).getSize!(cfg);
      const r = size[0] / 2;
      const styles = {
        x: 0,
        y: 0,
        r,
        ...style,
      };
      return styles;
    },
    update(cfg: ModelConfig, item: Item) {
      const group = item.getContainer();
      const metricLabel = group.get("children")[2]; // Get the shape which contains our label
      const metric = metricLabel.attr();
      metric.text = cfg.metric;
      metricLabel.attr(metric); // Update
    },
  },
  "single-node"
);
