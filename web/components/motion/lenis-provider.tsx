"use client";

import { ReactLenis } from "lenis/react";
import type { ReactNode } from "react";

/**
 * Smooth scrolling via Lenis.
 * DESIGN.md: must work in RTL (vertical scroll, no direction change needed),
 * disabled smoothing when prefers-reduced-motion (respectReducedMotion: true).
 * transform/opacity only — Lenis animates scroll, not layout.
 */
export function LenisProvider({ children }: { children: ReactNode }) {
  return (
    <ReactLenis
      root
      options={{
        autoRaf: true,
        lerp: 0.1,
        orientation: "vertical",
        gestureOrientation: "vertical",
        smoothWheel: true,
        syncTouch: false,
        respectReducedMotion: true,
      }}
    >
      {children}
    </ReactLenis>
  );
}
