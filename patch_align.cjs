const fs = require('fs');
const file = 'src/windows/editor/render/pixiCompositor.ts';
let code = fs.readFileSync(file, 'utf8');

const target = `
        // Center the video in the hole
        const videoX = holeRect.x - (videoWidth - holeRect.width) / 2;
        const videoY = holeRect.y - (videoHeight - holeRect.height) / 2;
`;

const replacement = `
        // Center the video horizontally, but align to the TOP vertically 
        // to prevent the macOS menu bar from being clipped by object-fit: cover
        const videoX = holeRect.x - (videoWidth - holeRect.width) / 2;
        const videoY = holeRect.y; // Align to top!
`;

code = code.replace(target, replacement);
fs.writeFileSync(file, code);
