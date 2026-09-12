const fs = require('fs');

const outerPath = "M 114 40 L 1086 40 A 24 24 0 0 1 1110 64 L 1110 686 A 24 24 0 0 1 1086 710 L 114 710 A 24 24 0 0 1 90 686 L 90 64 A 24 24 0 0 1 114 40 Z";
// Perfect notch
const innerPath = "M 1068 70 L 688 70 A 8 8 0 0 1 680 78 L 680 86 A 8 8 0 0 1 672 94 L 528 94 A 8 8 0 0 1 520 86 L 520 78 A 8 8 0 0 1 512 70 L 132 70 A 12 12 0 0 0 120 82 L 120 658 A 12 12 0 0 0 132 670 L 1068 670 A 12 12 0 0 0 1080 658 L 1080 82 A 12 12 0 0 0 1068 70 Z";

const rimOuter = "M 114 36 L 1086 36 A 28 28 0 0 1 1114 64 L 1114 686 A 28 28 0 0 1 1086 714 L 114 714 A 28 28 0 0 1 86 686 L 86 64 A 28 28 0 0 1 114 36 Z";
const rimInner = "M 1086 40 L 114 40 A 24 24 0 0 0 90 64 L 90 686 A 24 24 0 0 0 114 710 L 1086 710 A 24 24 0 0 0 1110 686 L 1110 64 A 24 24 0 0 0 1086 40 Z";

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <!-- Beautiful soft realistic drop shadow -->
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="30" stdDeviation="25" flood-color="#000000" flood-opacity="0.3"/>
      <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000000" flood-opacity="0.2"/>
    </filter>

    <linearGradient id="bezel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#141414"/>
      <stop offset="100%" stop-color="#020202"/>
    </linearGradient>

    <!-- Metallic Aluminum Rim Gradient (Midnight/Space Grey) -->
    <linearGradient id="alumLid" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#555b63"/>
      <stop offset="5%" stop-color="#808891"/>
      <stop offset="20%" stop-color="#494f57"/>
      <stop offset="50%" stop-color="#606770"/>
      <stop offset="80%" stop-color="#494f57"/>
      <stop offset="95%" stop-color="#808891"/>
      <stop offset="100%" stop-color="#555b63"/>
    </linearGradient>

    <linearGradient id="baseTop" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3a3f45"/>
      <stop offset="15%" stop-color="#5e656e"/>
      <stop offset="50%" stop-color="#737b85"/>
      <stop offset="85%" stop-color="#5e656e"/>
      <stop offset="100%" stop-color="#3a3f45"/>
    </linearGradient>

    <linearGradient id="baseLip" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1c1f24"/>
      <stop offset="15%" stop-color="#3a3f45"/>
      <stop offset="50%" stop-color="#4c545c"/>
      <stop offset="85%" stop-color="#3a3f45"/>
      <stop offset="100%" stop-color="#1c1f24"/>
    </linearGradient>

    <linearGradient id="screenGloss" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
    </linearGradient>
  </defs>

  <!-- 1. Drop Shadow Proxy -->
  <rect x="60" y="710" width="1080" height="24" rx="12" fill="#000" filter="url(#shadow)" opacity="0.8"/>

  <!-- 2. Aluminum Lid Rim (EvenOdd Path for the outer lip) -->
  <path
    fill="url(#alumLid)"
    fill-rule="evenodd"
    d="${rimOuter} ${rimInner}"
  />

  <!-- 3. Screen Bezel & Hole (EvenOdd Path for the bezel masking) -->
  <path
    fill="url(#bezel)"
    fill-rule="evenodd"
    d="${outerPath} ${innerPath}"
  />

  <!-- Rubber Gasket Outline -->
  <rect x="90" y="40" width="1020" height="670" rx="24" fill="none" stroke="#000" stroke-width="1.5" opacity="0.9"/>
  <!-- Inner Bezel edge reflection -->
  <rect x="120" y="70" width="960" height="600" rx="12" fill="none" stroke="#2a2a2a" stroke-width="0.5" opacity="0.6"/>

  <!-- 4. Base (Keyboard Deck + Hinge) -->
  <rect x="420" y="708" width="360" height="8" rx="3" fill="#111" opacity="0.95"/>
  <path d="M 86 714 L 1114 714 L 1160 740 A 6 6 0 0 1 1156 746 L 44 746 A 6 6 0 0 1 40 740 Z" fill="url(#baseTop)" />
  <path d="M 40 740 A 6 6 0 0 0 44 746 L 1156 746 A 6 6 0 0 0 1160 740 L 1160 744 A 6 6 0 0 1 1156 750 L 44 750 A 6 6 0 0 1 40 744 Z" fill="url(#baseLip)" />
  <path d="M 520 746 L 680 746 L 680 747 A 4 4 0 0 1 676 751 L 524 751 A 4 4 0 0 1 520 747 Z" fill="#2a2e33" opacity="0.9"/>

  <!-- 5. Camera & Sensors -->
  <!-- Main camera lens -->
  <circle cx="600" cy="82" r="5" fill="#050505"/>
  <circle cx="600" cy="82" r="2" fill="#1b2a49"/>
  <circle cx="601" cy="81" r="0.8" fill="#5c7bb5" opacity="0.7"/> <!-- Reflection -->
  
  <!-- Ambient light sensor -->
  <circle cx="585" cy="82" r="2" fill="#080808"/>
  
  <!-- Camera indicator LED (off) -->
  <circle cx="620" cy="82" r="2" fill="#0a1a10"/>
</svg>`;

fs.writeFileSync('public/mockups/macbook-8k.svg', svg);
