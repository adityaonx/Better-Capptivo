const fs = require('fs');
const file = 'src/windows/editor/render/pixiCompositor.ts';
let code = fs.readFileSync(file, 'utf8');

const target = `
        rect = {
          x: videoX,
          y: videoY,
          width: videoWidth,
          height: videoHeight,
        };
`;

const replacement = `
        // Add a tiny 2px uniform bleed to ensure no sub-pixel gaps 
        // or extreme edge rounding is visible on any side.
        const bleed = 2;
        rect = {
          x: videoX - bleed,
          y: videoY - bleed,
          width: videoWidth + bleed * 2,
          height: videoHeight + bleed * 2,
        };
`;

code = code.replace(target, replacement);
fs.writeFileSync(file, code);
