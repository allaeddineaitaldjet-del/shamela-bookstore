export const BACKEND_URL =
  process.env.BACKEND_URL || "http://localhost:8000";

export type BookRow = {
  work_id: number;
  title_ar: string;
  author: string | null;
  category_slugs: string[];
  price_dzd: number | null;
  in_stock: boolean;
  publisher: string | null;
  pages: number | null;
};

export type BookDetail = BookRow & {
  editor: string | null;
  volumes: number | null;
  year_hijri: number | null;
  year_gregorian: number | null;
};

export type CategoryRow = { slug: string; name_ar: string; name_fr: string };
export type WilayaRow = { code: number; name_ar: string; name_fr: string };

async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BACKEND_URL}/api${path}`, {
    next: { revalidate: 0 },
  });
  if (!res.ok) throw new Error(`API ${path} failed ${res.status}`);
  return res.json() as Promise<T>;
}

export function listBooks(params: { category?: string; q?: string; page?: number }) {
  const q = new URLSearchParams();
  if (params.category) q.set("category", params.category);
  if (params.q) q.set("q", params.q);
  q.set("page", String(params.page || 1));
  return getJSON<{ items: BookRow[]; count: number; page: number; page_size: number }>(
    `/books?${q.toString()}`,
  );
}

export function getBook(id: string) {
  return getJSON<BookDetail>(`/books/${id}`);
}

export function listCategories() {
  return getJSON<CategoryRow[]>("/categories");
}

export function listWilayas() {
  return getJSON<WilayaRow[]>("/wilayas");
}

export function formatPrice(price: number | null, locale: string): string {
  if (price === null || price === undefined) return "—";
  const digits = String(price).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  return locale === "ar" ? `${digits} د.ج` : `${digits} DA`;
}
