import { getTranslations } from "next-intl/server";
import { Suspense } from "react";

export default function OrderSuccessPage(props: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ id?: string }>;
}) {
  return (
    <Suspense fallback={null}>
      <OrderSuccessContent {...props} />
    </Suspense>
  );
}

async function OrderSuccessContent({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ id?: string }>;
}) {
  await params;
  const sp = (await searchParams?.catch(() => ({}))) as { id?: string } | undefined;
  const t = await getTranslations("Order");
  return (
    <main
      style={{
        maxWidth: 600,
        marginInlineStart: "auto",
        marginInlineEnd: "auto",
        paddingInlineStart: "1rem",
        paddingInlineEnd: "1rem",
        paddingBlockStart: "3rem",
        textAlign: "center",
      }}
    >
      <h1>{t("success")}</h1>
      {sp?.id && <p>#{sp.id}</p>}
    </main>
  );
}
