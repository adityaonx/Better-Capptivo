const fs = require('fs');
const file = 'src/windows/editor/render/pixiCompositor.ts';
let code = fs.readFileSync(file, 'utf8');

const target = `
        // Stretch the video to fill the hole, but bleed it by 2 pixels on all sides
        // This hides the video's native black rounded corners under the opaque bezel
        // without causing massive clipping of the menu bar or sides.
        const bleed = 2;
        rect = {
          x: holeRect.x - bleed,
          y: holeRect.y - bleed,
          width: holeRect.width + bleed * 2,
          height: holeRect.height + bleed * 2,
        };
`;

const replacement = `
        // object-fit: cover to preserve aspect ratio while filling the hole
        const holeAspect = holeRect.width / holeRect.height;
        let videoWidth = holeRect.width;
        let videoHeight = holeRect.height;
        if (inputs.sourceAspect > holeAspect) {
          // Video is wider than hole -> match height, scale width
          videoHeight = holeRect.height;
          videoWidth = holeRect.height * inputs.sourceAspect;
        } else {
          // Video is taller than hole -> match width, scale height
          videoWidth = holeRect.width;
          videoHeight = holeRect.width / inputs.sourceAspect;
        }
        
        // Center horizontally, but align flush to the TOP vertically.
        // This prevents the menu bar from being clipped by the top bezel,
        // while the horizontal bleed hides the native rounded corners of the video.
        const videoX = holeRect.x - (videoWidth - holeRect.width) / 2;
        const videoY = holeRect.y;

        rect = {
          x: videoX,
          y: videoY,
          width: videoWidth,
          height: videoHeight,
        };
`;

code = code.replace(target, replacement);
fs.writeFileSync(file, code);
