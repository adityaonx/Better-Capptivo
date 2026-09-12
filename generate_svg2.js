function innerHoleWithNotch(x, y, w, h, r, notchW, notchH, notchR) {
  const cx = x + w/2;
  const nx1 = cx - notchW/2;
  const nx2 = cx + notchW/2;
  
  return `
    M ${x+w-r} ${y}
    L ${nx2+notchR} ${y}
    A ${notchR} ${notchR} 0 0 1 ${nx2} ${y+notchR}
    L ${nx2} ${y+notchH-notchR}
    A ${notchR} ${notchR} 0 0 1 ${nx2-notchR} ${y+notchH}
    L ${nx1+notchR} ${y+notchH}
    A ${notchR} ${notchR} 0 0 1 ${nx1} ${y+notchH-notchR}
    L ${nx1} ${y+notchR}
    A ${notchR} ${notchR} 0 0 1 ${nx1-notchR} ${y}
    L ${x+r} ${y}
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

console.log("Inner hole with notch (counter-clockwise):");
console.log(innerHoleWithNotch(120, 70, 960, 600, 12, 160, 24, 8));
