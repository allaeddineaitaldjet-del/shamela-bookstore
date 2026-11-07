import { Reveal } from "@/components/motion/reveal";
import { useLocale, useTranslations } from "next-intl";

export default function HomePage() {
  const t = useTranslations("HomePage");
  const locale = useLocale();
  const dir = locale === "ar" ? "rtl" : "ltr";

  return (
    <main
      style={{
        paddingInlineStart: "2rem",
        paddingInlineEnd: "2rem",
        paddingBlockStart: "2rem",
        paddingBlockEnd: "2rem",
        textAlign: "start",
      }}
    >
      <Reveal dir={dir} delay={0}>
        <h1>{t("title")}</h1>
      </Reveal>
      <Reveal dir={dir} delay={0.1}>
        <p>{t("subtitle")}</p>
      </Reveal>
    </main>
  );
}
