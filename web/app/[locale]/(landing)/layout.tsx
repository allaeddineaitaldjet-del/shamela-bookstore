import { LandingHeader } from "@/components/landing-header";
import { SiteFooter } from "@/components/site-footer";

export default function LandingLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <LandingHeader />
      {children}
      <SiteFooter />
    </>
  );
}
