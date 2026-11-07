"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { BookCover } from "@/components/book-card";

const Hero3D = dynamic(() => import("@/components/hero-3d").then((m) => m.Hero3D), {
  ssr: false,
  loading: () => (
    <div style={{ aspectRatio: "2/3", maxHeight: 360, width: "100%" }}>
      <BookCover title="مكتبة الشاملة" author={null} />
    </div>
  ),
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

  if (!enabled) {
    return (
      <div id="hero-3d-slot" style={{ aspectRatio: "2/3", maxHeight: 360, width: "100%" }}>
        <BookCover title="مكتبة الشاملة" author={null} />
      </div>
    );
  }
  return (
    <div id="hero-3d-slot" style={{ aspectRatio: "4/3", maxHeight: 360, width: "100%" }}>
      {visible ? <Hero3D /> : <div style={{ height: "100%" }} />}
    </div>
  );
}
