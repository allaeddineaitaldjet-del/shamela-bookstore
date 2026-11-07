"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import type { WilayaRow } from "@/lib/api";

const PHONE_RE = /^(?:\+213|0)(5|6|7)\d{8}$/;

export function OrderForm({ workId }: { workId: number }) {
  const t = useTranslations("Order");
  const locale = useLocale();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [wilayas, setWilayas] = useState<WilayaRow[]>([]);

  useEffect(() => {
    fetch("/api/wilayas")
      .then((r) => r.json())
      .then(setWilayas)
      .catch(() => setWilayas([]));
  }, []);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    const fd = new FormData(e.currentTarget);
    const customer_name = String(fd.get("customer_name") || "").trim();
    const phone = String(fd.get("phone") || "").trim();
    const wilaya_code = Number(fd.get("wilaya_code"));
    const address = String(fd.get("address") || "").trim();
    const qty = Number(fd.get("qty") || 1);
    const normalized = phone.replace(/[\s\-()]/g, "").replace(/^\+213/, "0");
    if (!PHONE_RE.test(phone.replace(/[\s\-()]/g, "")) && !PHONE_RE.test(normalized)) {
      setError(locale === "ar" ? "رقم هاتف غير صحيح" : "Phone number invalid");
      return;
    }
    if (qty < 1 || qty > 10) {
      setError(locale === "ar" ? "الكمية من 1 إلى 10" : "Qty 1..10");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_name,
          phone,
          wilaya_code,
          address,
          items: [{ work_id: workId, qty }],
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const msg = data?.detail || data?.error || t("error");
        setError(typeof msg === "string" ? msg : JSON.stringify(msg));
        setLoading(false);
        return;
      }
      window.location.href = `/${locale}/order/success?id=${data.id}`;
    } catch {
      setError(t("error"));
      setLoading(false);
    }
  }

  const inputStyle: React.CSSProperties = {
    width: "100%",
    minHeight: 44,
    paddingInlineStart: "0.75rem",
    borderRadius: 6,
    border: "1px solid var(--line)",
    background: "var(--surface)",
    color: "var(--ink)",
    boxSizing: "border-box",
  };

  return (
    <form
      onSubmit={onSubmit}
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
        maxWidth: 480,
        marginBlockStart: "1.5rem",
      }}
    >
      <label style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
        {t("name")}
        <input name="customer_name" required style={inputStyle} />
      </label>
      <label style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
        {t("phone")}
        <input name="phone" required inputMode="tel" style={inputStyle} dir="ltr" />
      </label>
      <label style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
        {t("wilaya")}
        <select name="wilaya_code" required style={inputStyle}>
          {wilayas.map((w) => (
            <option key={w.code} value={w.code}>
              {w.code} — {locale === "ar" ? w.name_ar : w.name_fr}
            </option>
          ))}
        </select>
      </label>
      <label style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
        {t("address")}
        <textarea name="address" required style={{ ...inputStyle, minHeight: 80 }} />
      </label>
      <label style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
        {t("qty")}
        <input name="qty" type="number" min={1} max={10} defaultValue={1} required style={inputStyle} />
      </label>
      {error && (
        <p role="alert" style={{ color: "var(--accent)", margin: 0 }}>
          {error}
        </p>
      )}
      <button
        type="submit"
        disabled={loading}
        style={{
          minHeight: 44,
          borderRadius: 6,
          background: "var(--primary)",
          color: "#fff",
          border: "none",
          fontWeight: 700,
        }}
      >
        {t("submit")}
      </button>
    </form>
  );
}
