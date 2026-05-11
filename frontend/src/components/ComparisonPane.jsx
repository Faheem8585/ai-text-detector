export default function ComparisonPane({ value, onChange }) {
  return (
    <div className="panel">
      <div className="panel-title">calibration sample (optional)</div>
      <p className="text-[11px] text-slate-500 mb-2">
        paste your own writing here to soften the score against your
        baseline style.
      </p>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="optional"
        className="w-full h-32 bg-slate-950/60 border border-slate-800
                   rounded-lg p-3 text-xs focus:border-cyan-500
                   focus:outline-none focus:ring-1 focus:ring-cyan-500/30
                   placeholder:text-slate-600"
      />
      {value && (
        <div className="mt-2 text-[10px] text-emerald-400">
          {value.trim().split(/\s+/).length} words
        </div>
      )}
    </div>
  );
}
