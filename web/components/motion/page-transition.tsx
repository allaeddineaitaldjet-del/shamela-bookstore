"use client";

import { motion, useReducedMotion } from "motion/react";
import type { ReactNode } from "react";

/**
 * Page transition via Next.js template.tsx remount.
 * DESIGN.md: UI feedback 150-250ms, fade only, no layout shift.
 * Honours reduced motion (no movement).
 */
export function PageTransition({ children }: { children: ReactNode }) {
  const reduce = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: reduce ? 0.2 : 0.25, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
