import { LandingSections } from "@/components/landing-sections";
import { listBooks, listCategories } from "@/lib/api";
import { Suspense } from "react";

export default function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  return (
    <Suspense fallback={null}>
      <HomeContent params={params} />
    </Suspense>
  );
}

async function HomeContent({ params }: { params: Promise<{ locale: string }> }) {
  await params;
  const [cats, books] = await Promise.all([
    listCategories().catch(() => []),
    listBooks({ page: 1 }).catch(() => ({ items: [], count: 0 })),
  ]);
  return <LandingSections categories={cats} books={books.items} total={books.count} />;
}
