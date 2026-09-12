function roundedRectPath(x, y, w, h, r, clockwise=true) {
  if (clockwise) {
    return `
      M ${x+r} ${y}
      L ${x+w-r} ${y}
      A ${r} ${r} 0 0 1 ${x+w} ${y+r}
      L ${x+w} ${y+h-r}
      A ${r} ${r} 0 0 1 ${x+w-r} ${y+h}
      L ${x+r} ${y+h}
      A ${r} ${r} 0 0 1 ${x} ${y+h-r}
      L ${x} ${y+r}
      A ${r} ${r} 0 0 1 ${x+r} ${y}
      Z
    `.replace(/\s+/g, ' ').trim();
  } else {
    return `
      M ${x+r} ${y}
      A ${r} ${r} 0 0 0 ${x} ${y+r}
      L ${x} ${y+h-r}
      A ${r} ${r} 0 0 0 ${x+r} ${y+h}
      L ${x+w-r} ${y+h}
      A ${r} ${r} 0 0 0 ${x+w} ${y+h-r}
      L ${x+w} ${y+r}
      A ${r} ${r} 0 0 0 ${x+w-r} ${y}
      Z
    `.replace(/\s+/g, ' ').trim();
  }
}

console.log("Outer lid (clockwise):");
console.log(roundedRectPath(90, 40, 1020, 670, 24, true));

console.log("Inner hole (counter-clockwise):");
console.log(roundedRectPath(120, 70, 960, 600, 12, false));

