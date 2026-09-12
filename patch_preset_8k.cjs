const fs = require('fs');
const file = 'src/windows/editor/lib/mockupPresets.ts';

const scale = 8192 / 1200;

const code = `export interface MockupPreset {
  id: string;
  name: string;
  src: string;
  corners: [
    { x: number; y: number },
    { x: number; y: number },
    { x: number; y: number },
    { x: number; y: number },
  ];
  width: number;
  height: number;
}

export const MOCKUP_PRESETS: readonly MockupPreset[] = [
  {
    id: "macbook-flat",
    name: "MacBook Air",
    src: "/mockups/macbook-8k.svg",
    width: 8192,
    height: Math.round(800 * ${scale}),
    corners: [
      { x: Math.round(120 * ${scale}), y: Math.round(70 * ${scale}) },  // TL
      { x: Math.round(1080 * ${scale}), y: Math.round(70 * ${scale}) }, // TR
      { x: Math.round(1080 * ${scale}), y: Math.round(670 * ${scale}) },// BR
      { x: Math.round(120 * ${scale}), y: Math.round(670 * ${scale}) }, // BL
    ],
  },
];
`;

fs.writeFileSync(file, code);
