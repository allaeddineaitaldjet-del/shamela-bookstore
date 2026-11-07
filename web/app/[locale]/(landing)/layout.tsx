import { DarkNav } from "@/components/landing/dark-nav";
import { DarkBg } from "@/components/landing/dark-bg";
import { SiteFooter } from "@/components/site-footer";

export default function LandingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="landing-dark relative min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <DarkBg />
      <DarkNav />
      <div className="relative z-10">{children}</div>
      <div className="relative z-10">
        <SiteFooter />
      </div>
    </div>
  );
}