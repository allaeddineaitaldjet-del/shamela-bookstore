"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { BookCover } from "@/components/book-card";

// Lazy, client-only. The loading state already fills the same slot box.
const Hero3D = dynamic(() => import("@/components/hero-3d").then((m) => m.Hero3D), {
  ssr: false,
  loading: () => <FlatCover />,
});

function webglOK() {
  try {
    const c = document.createElement("canvas");
    return !!(
      window.WebGLRenderingContext &&
      (c.getContext("webgl") || c.getContext("experimental-webgl"))
    );
  } catch {
    return false;
  }
}

function FlatCover() {
  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="aspect-[2/3] h-full">
        <BookCover title="مكتبة الشاملة" author={null} />
      </div>
    </div>
  );
}

export function Hero3DWrapper() {
  const [enabled, setEnabled] = useState(false);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setEnabled(!mq.matches && webglOK());
    update();
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, []);

  useEffect(() => {
    const el = document.getElementById("hero-3d-slot");
    if (!el) return;
    const obs = new IntersectionObserver(
      (entries) => setVisible(entries[0].isIntersecting),
      { threshold: 0.05 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  // The fallback and the canvas share the exact same slot box: no layout jump.
  return (
    <div id="hero-3d-slot" className="relative h-full w-full">
      {enabled && visible ? <Hero3D /> : <FlatCover />}
    </div>
  );
}