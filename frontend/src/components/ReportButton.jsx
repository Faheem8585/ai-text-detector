import { useState } from "react";
import { downloadReport } from "../lib/api";

export default function ReportButton({ result }) {
  const [busy, setBusy] = useState(false);
  const [name, setName] = useState("");

  async function handle() {
    setBusy(true);
    try {
      await downloadReport(result, name.trim() || "untitled");
    } catch (e) {
      alert(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="panel">
      <div className="panel-title">export</div>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="case name (optional)"
        className="w-full bg-slate-950/60 border border-slate-800
                   rounded-lg p-2 text-xs focus:border-cyan-500
                   focus:outline-none placeholder:text-slate-600 mb-3"
      />
      <button onClick={handle} disabled={busy} className="btn-cyber w-full">
        {busy ? "generating..." : "download pdf"}
      </button>
    </div>
  );
}
