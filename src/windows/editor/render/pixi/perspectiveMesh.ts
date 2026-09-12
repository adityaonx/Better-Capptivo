import { MeshGeometry, Mesh, Texture } from "pixi.js";

type Point = { x: number; y: number };

function getPerspectiveTransform(p0: Point, p1: Point, p2: Point, p3: Point) {
  const dx1 = p1.x - p2.x;
  const dx2 = p3.x - p2.x;
  const dx3 = p0.x - p1.x + p2.x - p3.x;

  const dy1 = p1.y - p2.y;
  const dy2 = p3.y - p2.y;
  const dy3 = p0.y - p1.y + p2.y - p3.y;

  if (dx3 === 0 && dy3 === 0) {
    return [
      p1.x - p0.x, p3.x - p0.x, p0.x,
      p1.y - p0.y, p3.y - p0.y, p0.y,
      0, 0, 1,
    ];
  } else {
    const det = dx1 * dy2 - dx2 * dy1;
    if (det === 0) return null;

    const a13 = (dx3 * dy2 - dx2 * dy3) / det;
    const a23 = (dx1 * dy3 - dx3 * dy1) / det;

    return [
      p1.x - p0.x + a13 * p1.x, p3.x - p0.x + a23 * p3.x, p0.x,
      p1.y - p0.y + a13 * p1.y, p3.y - p0.y + a23 * p3.y, p0.y,
      a13, a23, 1,
    ];
  }
}

function project(m: number[], u: number, v: number): Point {
  const w = m[6] * u + m[7] * v + m[8];
  return {
    x: (m[0] * u + m[1] * v + m[2]) / w,
    y: (m[3] * u + m[4] * v + m[5]) / w,
  };
}

export function createPerspectiveMesh(
  texture: Texture,
  corners: [Point, Point, Point, Point],
  cols = 10,
  rows = 10
): Mesh {
  const transform = getPerspectiveTransform(corners[0], corners[1], corners[2], corners[3]);
  
  if (!transform) {
    // Fallback if invalid
    return new Mesh({ geometry: new MeshGeometry({ positions: new Float32Array([0,0,1,0,1,1,0,1]), uvs: new Float32Array([0,0,1,0,1,1,0,1]), indices: new Uint32Array([0,1,2, 0,2,3]) }), texture });
  }

  const vertices: number[] = [];
  const uvs: number[] = [];
  const indices: number[] = [];

  for (let r = 0; r <= rows; r++) {
    const v = r / rows;
    for (let c = 0; c <= cols; c++) {
      const u = c / cols;
      const p = project(transform, u, v);
      vertices.push(p.x, p.y);
      uvs.push(u, v);
    }
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i0 = r * (cols + 1) + c;
      const i1 = i0 + 1;
      const i2 = (r + 1) * (cols + 1) + c;
      const i3 = i2 + 1;

      // Two triangles per cell
      indices.push(i0, i1, i2);
      indices.push(i1, i3, i2);
    }
  }

  const geometry = new MeshGeometry({
    positions: new Float32Array(vertices),
    uvs: new Float32Array(uvs),
    indices: new Uint32Array(indices)
  });
  

  return new Mesh({ geometry, texture });
}

export function updatePerspectiveMesh(
  mesh: Mesh,
  corners: [Point, Point, Point, Point],
  cols = 10,
  rows = 10
) {
  const transform = getPerspectiveTransform(corners[0], corners[1], corners[2], corners[3]);
  if (!transform) return;

  const positions = mesh.geometry.getBuffer("aPosition").data as Float32Array;
  let i = 0;
  for (let r = 0; r <= rows; r++) {
    const v = r / rows;
    for (let c = 0; c <= cols; c++) {
      const u = c / cols;
      const p = project(transform, u, v);
      positions[i++] = p.x;
      positions[i++] = p.y;
    }
  }

  mesh.geometry.getBuffer("aPosition").update();
}
