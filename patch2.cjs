const fs = require('fs');
const file = 'src/windows/editor/render/pixiCompositor.ts';
let code = fs.readFileSync(file, 'utf8');

const target = `
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d")!;
  ctx.drawImage(img, 0, 0, w, h);
`;

const replacement = `
  const scale = 2; // Rasterize at 2x resolution for zoom crispness
  const canvas = document.createElement("canvas");
  canvas.width = w * scale;
  canvas.height = h * scale;
  const ctx = canvas.getContext("2d")!;
  ctx.scale(scale, scale);
  ctx.drawImage(img, 0, 0, w, h);
`;

code = code.replace(target, replacement);
fs.writeFileSync(file, code);
