import { IGroup, IShape } from "@antv/g-canvas/lib/interfaces";
import G6, { ModelConfig } from "@antv/g6";

const lineDash = [4, 2, 1, 2];
G6.registerEdge(
  "line-dash",
  {
    afterDraw(cfg?: ModelConfig, group?: IGroup, rst?: IShape) {
      const shape = group!.get("children")[0];
      let index = 0;
      shape.animate(
        () => {
          index++;
          if (index > 9) {
            index = 0;
          }
          const res = {
            lineDash,
            lineDashOffset: -index,
          };
          return res;
        },
        {
          repeat: true,
          duration: 3000,
        }
      );
    },
  },
  "cubic-horizontal"
);
