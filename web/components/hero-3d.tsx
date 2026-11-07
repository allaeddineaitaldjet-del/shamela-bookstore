"use client";

import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

function makeCoverTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 768;
  const ctx = canvas.getContext("2d");
  if (!ctx) return null;
  ctx.fillStyle = "#1F5C4A";
  ctx.fillRect(0, 0, 512, 768);
  ctx.strokeStyle = "#B5532F";
  ctx.lineWidth = 6;
  ctx.strokeRect(20, 20, 472, 728);
  ctx.strokeStyle = "#B8913A";
  ctx.lineWidth = 2;
  ctx.strokeRect(36, 36, 440, 696);
  // eight-pointed star motif (simple)
  ctx.strokeStyle = "#B8913A";
  ctx.beginPath();
  const cx = 256;
  const cy = 300;
  const r = 70;
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI) / 4;
    ctx.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r);
    const a2 = a + Math.PI / 8;
    ctx.lineTo(cx + Math.cos(a2) * r * 0.5, cy + Math.sin(a2) * r * 0.5);
  }
  ctx.stroke();
  ctx.fillStyle = "#F6EFE0";
  ctx.font = "bold 42px serif";
  ctx.textAlign = "center";
  ctx.fillText("مكتبة الشاملة", cx, 520);
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  tex.needsUpdate = true;
  return tex;
}

function Book() {
  const group = useRef<THREE.Group>(null!);
  const tex = makeCoverTexture();
  useFrame((state, delta) => {
    const t = state.clock.elapsedTime;
    group.current.position.y = Math.sin(t * 0.8) * 0.08;
    const p = state.pointer;
    group.current.rotation.y = -0.4 + p.x * 0.4;
    group.current.rotation.x = -0.2 + p.y * 0.2;
    // scroll progress: rotate 90deg over scroll length
    const prog = Math.min(1, window.scrollY / 1200);
    group.current.rotation.y += prog * 0.6;
  });
  return (
    <group ref={group}>
      {/* pages block cream */}
      <mesh position={[0.04, 0, 0]}>
        <boxGeometry args={[1.2, 1.8, 0.22]} />
        <meshStandardMaterial color="#FFFBF2" />
      </mesh>
      {/* cover green */}
      <mesh position={[0, 0, 0.13]}>
        <boxGeometry args={[1.24, 1.84, 0.02]} />
        {tex ? (
          <meshStandardMaterial map={tex} />
        ) : (
          <meshStandardMaterial color="#1F5C4A" />
        )}
      </mesh>
      {/* terracotta frame hint: thin box behind */}
      <mesh position={[0, 0, -0.13]}>
        <boxGeometry args={[1.24, 1.84, 0.02]} />
        <meshStandardMaterial color="#B5532F" />
      </mesh>
    </group>
  );
}

export function Hero3D() {
  return (
    <Canvas
      camera={{ position: [0, 0, 3.2], fov: 40 }}
      dpr={[1, 1.5]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <ambientLight intensity={0.7} />
      <directionalLight position={[3, 4, 5]} intensity={1.2} />
      <Book />
    </Canvas>
  );
}
