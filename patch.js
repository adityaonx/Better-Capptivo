const fs = require('fs');
const file = 'src/windows/editor/render/pixiCompositor.ts';
let code = fs.readFileSync(file, 'utf8');

const target = `
        rect = {
          x: mockupRect.x + tl.x * scaleX,
          y: mockupRect.y + tl.y * scaleY,
          width: (br.x - tl.x) * scaleX,
          height: (br.y - tl.y) * scaleY,
        };
      } else {
`;

const replacement = `
        const holeRect = {
          x: mockupRect.x + tl.x * scaleX,
          y: mockupRect.y + tl.y * scaleY,
          width: (br.x - tl.x) * scaleX,
          height: (br.y - tl.y) * scaleY,
        };

        // object-fit: cover the hole with the video to prevent squishing and hide native corners
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
        
        // Center the video in the hole
        const videoX = holeRect.x - (videoWidth - holeRect.width) / 2;
        const videoY = holeRect.y - (videoHeight - holeRect.height) / 2;

        rect = {
          x: videoX,
          y: videoY,
          width: videoWidth,
          height: videoHeight,
        };

        // We also need to store holeRect somewhere so we can use it for the mask!
        // But rect is used for camera zoom... 
        // Wait, if rect is the video bounds, the camera will zoom around the video.
        // That's fine! But we need to mask it.
        // Let's attach holeRect to inputs or a local variable.
        (inputs as any)._holeRect = holeRect;
      } else {
`;

code = code.replace(target, replacement);

const targetMask = `
      if (preset && mockupRect) {
        mockupSprite.texture = texture;
        mockupSprite.position.set(mockupRect.x, mockupRect.y);
        mockupSprite.width = mockupRect.width;
        mockupSprite.height = mockupRect.height;
        mockupSprite.visible = true;

        screenMask.set(rect.x, rect.y, rect.width, rect.height, 0);
        screenSprite.alpha = 1;
`;

const replaceMask = `
      if (preset && mockupRect) {
        mockupSprite.texture = texture;
        mockupSprite.position.set(mockupRect.x, mockupRect.y);
        mockupSprite.width = mockupRect.width;
        mockupSprite.height = mockupRect.height;
        mockupSprite.visible = true;

        const hr = (inputs as any)._holeRect || rect;
        // Expand the holeRect mask by 2 pixels so it completely tucks under the PNG bezel
        // This prevents any sharp edge of the mask from peaking out if there's a floating point gap
        screenMask.set(hr.x - 2, hr.y - 2, hr.width + 4, hr.height + 4, 0);
        screenSprite.alpha = 1;
`;

code = code.replace(targetMask, replaceMask);
fs.writeFileSync(file, code);
