"use client";

import { useRef, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

function makeCoverTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 768;
  const ctx = canvas.getContext("2d");
  if (!ctx) return null;

  // Base cover
  ctx.fillStyle = "#1F5C4A";
  ctx.fillRect(0, 0, 512, 768);

  // Frame
  ctx.strokeStyle = "#B5532F";
  ctx.lineWidth = 6;
  ctx.strokeRect(20, 20, 472, 728);
  ctx.strokeStyle = "#B8913A";
  ctx.lineWidth = 2;
  ctx.strokeRect(36, 36, 440, 696);

  // Eight-pointed star motif
  ctx.strokeStyle = "#B8913A";
  ctx.lineWidth = 2;
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

  // Store name
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

  // Track mouse from window (not canvas pointer events)
  const mouseRef = useRef({ x: 0, y: 0 });
  const targetRot = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      // Normalise -1..1
      mouseRef.current.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouseRef.current.y = -(e.clientY / window.innerHeight) * 2 + 1;
    };
    window.addEventListener("pointermove", handler);
    return () => window.removeEventListener("pointermove", handler);
  }, []);

  useFrame((state, delta) => {
    const t = state.clock.elapsedTime;
    const m = mouseRef.current;

    // Gentle idle float
    group.current.position.y = Math.sin(t * 0.6) * 0.06;

    // Scroll progress: rotate a little as the hero leaves the viewport.
    const prog = Math.min(1, window.scrollY / 1200);

    // Idle tilt + pointer influence + scroll offset (target is absolute, not incremental).
    targetRot.current.x = -0.15 + m.y * 0.35;
    targetRot.current.y = -0.3 + m.x * 0.35 + prog * 0.5;

    // Smooth interpolation (clamp dt so a long frame cannot overshoot).
    const speed = 2.5;
    const k = Math.min(delta, 0.05) * speed;
    group.current.rotation.x += (targetRot.current.x - group.current.rotation.x) * k;
    group.current.rotation.y += (targetRot.current.y - group.current.rotation.y) * k;
  });

  return (
    <group ref={group}>
      {/* Pages block cream */}
      <mesh position={[0.05, 0, 0]}>
        <boxGeometry args={[1.4, 2.1, 0.26]} />
        <meshStandardMaterial color="#FFFBF2" />
      </mesh>

      {/* Page-edge lines */}
      <mesh position={[0.04, 0, 0]}>
        <boxGeometry args={[1.38, 2.08, 0.002]} />
        <meshStandardMaterial color="#E8DFC8" />
      </mesh>
      <mesh position={[0.03, 0, 0]}>
        <boxGeometry args={[1.36, 2.06, 0.002]} />
        <meshStandardMaterial color="#E2D8C2" />
      </mesh>

      {/* Cover green */}
      <mesh position={[0, 0, 0.15]}>
        <boxGeometry args={[1.44, 2.14, 0.025]} />
        {tex ? (
          <meshStandardMaterial map={tex} roughness={0.6} metalness={0.1} />
        ) : (
          <meshStandardMaterial color="#1F5C4A" roughness={0.6} metalness={0.1} />
        )}
      </mesh>

      {/* Spine — visible on the left edge */}
      <mesh position={[-0.73, 0, 0]}>
        <boxGeometry args={[0.02, 2.14, 0.26]} />
        <meshStandardMaterial color="#1A4E3F" roughness={0.7} metalness={0.1} />
      </mesh>

      {/* Terracotta frame hint: thin box behind */}
      <mesh position={[0, 0, -0.15]}>
        <boxGeometry args={[1.44, 2.14, 0.025]} />
        <meshStandardMaterial color="#B5532F" roughness={0.8} />
      </mesh>
    </group>
  );
}

export function Hero3D() {
  return (
    <Canvas
      camera={{ position: [0, 0, 3.8], fov: 38 }}
      dpr={[1, 1.5]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      {/* Ambient soft fill */}
      <ambientLight intensity={0.5} />

      {/* Emerald rim light (left/back) */}
      <pointLight position={[-3, 2, 3]} intensity={0.6} color="#1F5C4A" distance={10} />

      {/* Warm key light (right/front) */}
      <directionalLight position={[4, 5, 6]} intensity={1.0} color="#FFFBF2" />

      {/* Subtle fill */}
      <pointLight position={[2, -1, 3]} intensity={0.25} color="#A98B4E" distance={8} />

      <Book />
    </Canvas>
  );
}