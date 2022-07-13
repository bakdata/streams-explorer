import { IGroup, IShape } from "@antv/g-base";
import G6, {
  Item,
  ModelConfig,
  NodeConfig,
  ShapeOptions,
  ShapeStyle,
} from "@antv/g6";
import { mix } from "@antv/util";

/* Custom G6 node to display applications
 * based on builtin modelRect node
 * https://github.com/antvis/G6/blob/4.6.15/packages/element/src/nodes/modelRect.ts
 */

G6.registerNode(
  "AppNode",
  {
    options: {
      size: [120, 50],
      style: {
        radius: 5,
        stroke: "#000", // border
        fill: "#fff",
        lineWidth: 2,
        fillOpacity: 0.05,
      },
      labelCfg: {
        style: {
          fill: "#000",
        },
      },
      logoIcon: {
        show: true,
        x: 0,
        y: 0,
        img: "",
        width: 36,
        height: 36,
        offset: 4,
      },
      stateIcon: {
        show: true,
        x: 0,
        y: 0,
        img: "",
        width: 20,
        height: 20,
        offset: -5,
      },
    },
    shapeType: "modelRect",
    drawShape(cfg?: ModelConfig, group?: IGroup): IShape {
      const style = (this as any).getShapeStyle!(cfg);
      const name = `${(this as ShapeOptions).type}-keyShape`;

      const keyShape = group!.addShape("rect", {
        attrs: style,
        className: name,
        name: name,
        draggable: true,
      });
      (group as any)["shapeMap"][name] = keyShape;

      (this as any).drawLogoIcon(cfg, group);
      (this as any).drawStateIcon(cfg, group);
      (this as any).drawMetricsLabel(group);

      return keyShape;
    },
    drawMetricsLabel(group: IGroup) {
      (group as any)["shapeMap"]["metric-label"] = group.addShape("text", {
        attrs: {
          textBaseline: "top",
          y: 50,
          lineHeight: 20,
          text: "",
          fill: "#333",
          fontStyle: "italic",
          textAlign: "center",
        },
        name: "metric",
      });
    },
    drawLogoIcon(cfg: NodeConfig, group: IGroup) {
      const { logoIcon = {} } = (this as any).mergeStyle
        || (this as any).getOptions(cfg) as NodeConfig;
      const size = (this as ShapeOptions).getSize!(cfg);
      const width = size[0];

      if (logoIcon.show) {
        const { width: w, height: h, x, y, offset, text, ...logoIconStyle } =
          logoIcon;
        const iconImg = cfg!.node_type + ".svg";
        (group as any)["shapeMap"]["rect-logo-icon"] = group.addShape("image", {
          attrs: {
            ...logoIconStyle,
            x: -width / 2 + (offset as number),
            y: -(h as number) / 2,
            width: w,
            height: h,
            img: iconImg,
          },
          className: "rect-logo-icon",
          name: "rect-logo-icon",
          draggable: true,
        });
      }
    },
    drawStateIcon(cfg: NodeConfig, group: IGroup) {
      const { stateIcon = {} } = (this as any).mergeStyle
        || (this as any).getOptions(cfg) as NodeConfig;
      const size = (this as ShapeOptions).getSize!(cfg);
      const width = size[0];

      if (stateIcon.show) {
        const { width: w, height: h, x, y, offset, text, ...iconStyle } =
          stateIcon;
        if (text) {
          (group as any)["shapeMap"]["rect-state-icon"] = group.addShape(
            "text",
            {
              attrs: {
                x: 0,
                y: 0,
                fontSize: 12,
                fill: "#000",
                stroke: "#000",
                textBaseline: "middle",
                textAlign: "center",
                ...iconStyle,
              },
              className: "rect-state-icon",
              name: "rect-state-icon",
              draggable: true,
            }
          );
        } else {
          (group as any)["shapeMap"]["rect-state-icon"] = group.addShape(
            "image",
            {
              attrs: {
                ...iconStyle,
                x: x || width / 2 - (w as number) + (offset as number),
                y: y || -(h as number) / 2,
                width: w,
                height: h,
              },
              className: "rect-state-icon",
              name: "rect-state-icon",
              draggable: true,
            }
          );
        }
      }
    },
    drawLabel(cfg: ModelConfig, group: IGroup): IShape {
      const { labelCfg = {} } = (this as any)
        .getOptions(
          cfg
        ) as NodeConfig;

      const { style: fontStyle } = labelCfg;
      const height = (this as ShapeOptions).getSize!(cfg)[1];

      const label = group.addShape("text", {
        attrs: {
          ...fontStyle,
          y: height / 2 + 22,
          text: cfg.label,
          textAlign: "center",
        },
        className: "text-shape",
        name: "text-shape",
        draggable: true,
        labelRelated: true,
      });

      (group as any)["shapeMap"]["text-shape"] = label;

      return label;
    },
    getShapeStyle(cfg: NodeConfig) {
      const { style: defaultStyle } = (this as any).mergeStyle
        || (this as any).getOptions(cfg) as NodeConfig;
      const strokeStyle: ShapeStyle = {
        stroke: cfg.color,
      };
      const style: ShapeStyle = mix({}, defaultStyle, strokeStyle);
      const size = (this as ShapeOptions).getSize!(cfg);
      const width = style.width || size[0];
      const height = style.height || size[1];
      const styles = {
        x: -width / 2,
        y: -height / 2,
        width,
        height,
        ...style,
      };
      return styles;
    },
    update(cfg: ModelConfig, item: Item) {
      const { style = {} } = (this as any).mergeStyle
        || (this as any).getOptions(cfg) as NodeConfig;
      const size = (this as ShapeOptions).getSize!(cfg);
      const width = size[0];
      const height = size[1];
      const keyShape = item.get("keyShape");
      keyShape.attr({
        ...style,
        x: -width / 2,
        y: -height / 2,
        width,
        height,
      });

      const group = item.getContainer();

      // update metric
      const metricLabelShape = (group as any)["shapeMap"]["metric-label"]
        || group.find(
          (element) => element.get("className") === "metric-label"
        );
      const metric = metricLabelShape.attr();
      metric.text = cfg.metric;
      metricLabelShape.attr(metric);

      const logoIconShape = (group as any)["shapeMap"]["rect-logo-icon"]
        || group.find((element) =>
          element.get("className") === "rect-logo-icon"
        );
      const currentLogoIconAttr = logoIconShape ? logoIconShape.attr() : {};

      const logoIcon = mix({}, currentLogoIconAttr, cfg.logoIcon);

      let { width: w } = logoIcon;
      if (w === undefined) {
        w = (this as any).options.logoIcon.width;
      }

      const stateIconShape = (group as any)["shapeMap"]["rect-state-icon"]
        || group.find(
          (element) => element.get("className") === "rect-state-icon"
        );
      const currentStateIconAttr = stateIconShape ? stateIconShape.attr() : {};
      const stateIcon = mix({}, currentStateIconAttr, cfg.stateIcon);
      if (stateIconShape) {
        if (!stateIcon.show && stateIcon.show !== undefined) {
          stateIconShape.remove();
          delete (group as any)["shapeMap"]["rect-state-icon"];
        }
        const {
          width: stateW,
          height: h,
          x,
          y,
          offset: stateOffset,
          ...stateIconStyle
        } = stateIcon;
        stateIconShape.attr({
          ...stateIconStyle,
          x: x || width / 2 - stateW + stateOffset,
          y: y || -h / 2,
          width: stateW,
          height: h,
        });
      } else if (stateIcon.show) {
        (this as any).drawStateIcon(cfg, group);
      }
    },
  },
  "single-node"
);
