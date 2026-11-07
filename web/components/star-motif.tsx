export function StarMotif({ size = 16 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      aria-hidden="true"
      style={{ opacity: 0.9 }}
    >
      <path
        d="M16 2 L19 11 L28 5 L21 13 L30 16 L21 19 L28 27 L19 21 L16 30 L13 21 L4 27 L11 19 L2 16 L11 13 L4 5 L13 11 Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.2"
      />
    </svg>
  );
}
