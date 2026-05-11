const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function analyze({ file, text, humanBaseline }) {
  const fd = new FormData();
  if (file) fd.append("file", file);
  if (text) fd.append("text", text);
  if (humanBaseline) fd.append("human_baseline", humanBaseline);

  const r = await fetch(`${BASE}/analyze`, { method: "POST", body: fd });
  if (!r.ok) {
    const detail = await r.json().catch(() => ({}));
    throw new Error(detail.detail || `analysis failed (${r.status})`);
  }
  return r.json();
}

export async function downloadReport(result, caseName = "untitled") {
  const r = await fetch(`${BASE}/report`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ result, case_name: caseName }),
  });
  if (!r.ok) throw new Error("report generation failed");
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `aegis-report-${caseName}.pdf`;
  a.click();
  URL.revokeObjectURL(url);
}
