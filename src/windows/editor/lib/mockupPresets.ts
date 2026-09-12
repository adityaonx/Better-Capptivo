export interface MockupPreset {
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
    src: "/mockups/Macbook_Mock.svg",
    width: 2048,
    height: 1241,
    corners: [
      { x: 207, y: 35 },
      { x: 1842, y: 35 },
      { x: 1842, y: 1097 },
      { x: 207, y: 1097 },
    ],
  },
];
