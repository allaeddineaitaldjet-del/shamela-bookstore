import { hasLocale } from "next-intl";
import { getRequestConfig } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "./routing";

export default getRequestConfig(async ({ locale }) => {
  const localeValue = locale ?? (await import("next/root-params").then((m) => m.locale()));
  if (!hasLocale(routing.locales, localeValue)) {
    notFound();
  }
  return {
    locale: localeValue,
    messages: (await import(`../messages/${localeValue}.json`)).default,
  };
});
