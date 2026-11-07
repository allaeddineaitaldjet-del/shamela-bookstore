"use client";

import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useLenis } from "lenis/react";

gsap.registerPlugin(ScrollTrigger);

/**
 * Connect Lenis scroll to GSAP ScrollTrigger.
 * Must be used inside <ReactLenis root>, only on landing components.
 */
export function useLenisScrollTrigger() {
  const lenis = useLenis();
  useEffect(() => {
    if (!lenis) return;
    const onScroll = () => ScrollTrigger.update();
    lenis.on("scroll", onScroll);
    return () => lenis.off("scroll", onScroll);
  }, [lenis]);
}
