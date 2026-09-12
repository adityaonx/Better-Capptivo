const fs = require('fs');
const file = 'src/windows/editor/render/pixiCompositor.ts';
let code = fs.readFileSync(file, 'utf8');

const target = `
      // DEBUG TEXT OVERLAY
      if (!inputs._debugText) {
        const { Text } = require("pixi.js");
        inputs._debugText = new Text({ text: "", style: { fill: 0xff0000, fontSize: 36, zIndex: 9999 } });
        stage.addChild(inputs._debugText);
      }
      if (preset) {
        inputs._debugText.text = "mockupRect: " + mockupRect.width.toFixed(1) + "x" + mockupRect.height.toFixed(1) + 
          "\\nrect: " + rect.width.toFixed(1) + "x" + rect.height.toFixed(1) + 
          "\\npreset: " + preset.width + "x" + preset.height +
          "\\nscaleX: " + (mockupRect.width / preset.width).toFixed(3) +
          "\\ntls: " + preset.corners[0].x + "," + preset.corners[0].y +
          "\\nsrcSize: " + inputs.sourceVideoSize.width + "x" + inputs.sourceVideoSize.height +
          "\\nvideoAspect: " + inputs.sourceAspect.toFixed(3) +
          "\\nholeAspect: " + ((inputs as any)._holeRect.width / (inputs as any)._holeRect.height).toFixed(3);
      }
      
      setCameraTransform(
        computeCameraTransform({
`;

const replacement = `
      setCameraTransform(
        computeCameraTransform({
`;

code = code.replace(target, replacement);
fs.writeFileSync(file, code);
