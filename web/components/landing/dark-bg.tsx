export function DarkBg() {
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 z-0 overflow-hidden"
    >
      {/* Layer 1: two drifting emerald radial lights (transform only) */}
      <span className="emerald-light emerald-light--1 absolute inset-0" />
      <span className="emerald-light emerald-light--2 absolute inset-0" />

      {/* Layer 2: feTurbulence noise at ~5% */}
      <svg className="absolute inset-0 h-full w-full opacity-5" width="100%" height="100%">
        <filter id="landing-noise">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.8"
            numOctaves="4"
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#landing-noise)" />
      </svg>

      {/* Layer 3: subtle vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_40%,rgba(0,0,0,0.4)_100%)]" />
    </div>
  );
}