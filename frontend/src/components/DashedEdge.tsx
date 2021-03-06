import G6 from "@antv/g6";
import { ModelConfig } from "@antv/g6/lib/types";
import GGroup from "@antv/g-canvas/lib/group";
import { IShape } from "@antv/g-canvas/lib/interfaces";

const lineDash = [4, 2, 1, 2];
G6.registerEdge(
  "line-dash",
  {
    afterDraw(cfg?: ModelConfig, group?: GGroup, rst?: IShape) {
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
