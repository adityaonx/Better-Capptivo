const fs = require('fs');

const outerPath = "M 114 40 L 1086 40 A 24 24 0 0 1 1110 64 L 1110 686 A 24 24 0 0 1 1086 710 L 114 710 A 24 24 0 0 1 90 686 L 90 64 A 24 24 0 0 1 114 40 Z";
const innerPath = "M 1068 70 L 688 70 A 8 8 0 0 1 680 78 L 680 86 A 8 8 0 0 1 672 94 L 528 94 A 8 8 0 0 1 520 86 L 520 78 A 8 8 0 0 1 512 70 L 132 70 A 12 12 0 0 0 120 82 L 120 658 A 12 12 0 0 0 132 670 L 1068 670 A 12 12 0 0 0 1080 658 L 1080 82 A 12 12 0 0 0 1068 70 Z";

// Outer aluminum rim path is just a slightly larger version of outerPath
const rimOuter = "M 114 36 L 1086 36 A 28 28 0 0 1 1114 64 L 1114 686 A 28 28 0 0 1 1086 714 L 114 714 A 28 28 0 0 1 86 686 L 86 64 A 28 28 0 0 1 114 36 Z";
const rimInner = "M 1086 40 L 114 40 A 24 24 0 0 0 90 64 L 90 686 A 24 24 0 0 0 114 710 L 1086 710 A 24 24 0 0 0 1110 686 L 1110 64 A 24 24 0 0 0 1086 40 Z";

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="120%">
      <feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#000000" flood-opacity="0.4"/>
      <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#000000" flood-opacity="0.2"/>
    </filter>

    <linearGradient id="bezel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#141414"/>
      <stop offset="100%" stop-color="#050505"/>
    </linearGradient>

    <linearGradient id="alumLid" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8ba2b8"/>
      <stop offset="15%" stop-color="#a4b8c9"/>
      <stop offset="50%" stop-color="#d0dee8"/>
      <stop offset="85%" stop-color="#a4b8c9"/>
      <stop offset="100%" stop-color="#8ba2b8"/>
    </linearGradient>

    <linearGradient id="baseTop" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#73899d"/>
      <stop offset="15%" stop-color="#93a9be"/>
      <stop offset="50%" stop-color="#c1d1df"/>
      <stop offset="85%" stop-color="#93a9be"/>
      <stop offset="100%" stop-color="#73899d"/>
    </linearGradient>

    <linearGradient id="baseLip" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#556677"/>
      <stop offset="15%" stop-color="#73899d"/>
      <stop offset="50%" stop-color="#a2b3c4"/>
      <stop offset="85%" stop-color="#73899d"/>
      <stop offset="100%" stop-color="#556677"/>
    </linearGradient>
  </defs>

  <!-- 1. Drop Shadow -->
  <!-- We apply shadow to a proxy shape that covers the laptop base -->
  <rect x="50" y="710" width="1100" height="24" rx="12" fill="#000" filter="url(#shadow)" opacity="0.8"/>

  <!-- 2. Aluminum Lid Rim (EvenOdd Path) -->
  <path
    fill="url(#alumLid)"
    fill-rule="evenodd"
    d="${rimOuter} ${rimInner}"
  />

  <!-- 3. Screen Bezel & Hole (EvenOdd Path) -->
  <path
    fill="url(#bezel)"
    fill-rule="evenodd"
    d="${outerPath} ${innerPath}"
  />

  <!-- Inner screen drop shadow (adds depth to the bezel edge) -->
  <rect x="120" y="70" width="960" height="600" rx="12" fill="none" stroke="#000" stroke-width="2" opacity="0.6"/>

  <!-- Rubber Gasket (Thin line inside alum edge) -->
  <rect x="90" y="40" width="1020" height="670" rx="24" fill="none" stroke="#000" stroke-width="1.5" opacity="0.8"/>

  <!-- 4. Base (Keyboard Deck + Hinge) -->
  <!-- Hinge -->
  <rect x="420" y="708" width="360" height="8" rx="3" fill="#222" opacity="0.9"/>
  
  <!-- Base Top (Angles slightly outward) -->
  <path d="M 86 714 L 1114 714 L 1160 740 A 6 6 0 0 1 1156 746 L 44 746 A 6 6 0 0 1 40 740 Z" fill="url(#baseTop)" />

  <!-- Base Front Lip (Vertical thickness) -->
  <path d="M 40 740 A 6 6 0 0 0 44 746 L 1156 746 A 6 6 0 0 0 1160 740 L 1160 744 A 6 6 0 0 1 1156 750 L 44 750 A 6 6 0 0 1 40 744 Z" fill="url(#baseLip)" />

  <!-- Trackpad indent (thumb groove) -->
  <path d="M 520 746 L 680 746 L 680 747 A 4 4 0 0 1 676 751 L 524 751 A 4 4 0 0 1 520 747 Z" fill="#556677" opacity="0.9"/>

  <!-- 5. Camera details -->
  <circle cx="600" cy="82" r="5" fill="#080808"/>
  <circle cx="600" cy="82" r="2" fill="#1b2a49"/>
  <circle cx="585" cy="82" r="2" fill="#080808"/>
  <circle cx="620" cy="82" r="2" fill="#22c55e" opacity="0.85"/>
</svg>`;

fs.writeFileSync('public/mockups/macbook-flat.svg', svg);
