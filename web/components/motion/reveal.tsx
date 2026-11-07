"use client";

import { motion, useReducedMotion } from "motion/react";
import type { ReactNode } from "react";

type RevealProps = {
  children: ReactNode;
  dir?: "rtl" | "ltr";
  delay?: number;
};

/**
 * Scroll reveal that respects RTL + reduced motion.
 * DESIGN.md: transform + opacity only, entrances 400-700ms ease-out.
 * RTL: slide comes from the reading-direction side (flip x when dir="rtl").
 */
export function Reveal({ children, dir = "ltr", delay = 0 }: RevealProps) {
  const reduce = useReducedMotion();
  const xStart = dir === "rtl" ? 24 : -24;

  if (reduce) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "0px 0px -80px 0px" }}
        transition={{ duration: 0.4, delay, ease: "easeOut" }}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: xStart }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "0px 0px -80px 0px" }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
