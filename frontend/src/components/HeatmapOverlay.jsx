export default function HeatmapOverlay({ heatmap = [], matched = [], hedges = [] }) {
  if (!heatmap.length) return null;

  const pps = heatmap.map((h) => h.perplexity_proxy);
  const min = Math.min(...pps);
  const max = Math.max(...pps);
  const span = Math.max(1, max - min);

  function bg(p) {
    const norm = 1 - (p - min) / span; // closer to min → "hotter"
    const a = Math.max(0, Math.min(0.55, norm * 0.55));
    return `rgba(248, 113, 113, ${a.toFixed(3)})`;
  }

  return (
    <div className="panel">
      <div className="panel-title">heatmap</div>
      <p className="leading-7 text-sm">
        {heatmap.map((h, i) => (
          <span
            key={i}
            title={`perplexity proxy ≈ ${h.perplexity_proxy}`}
            style={{ background: bg(h.perplexity_proxy) }}
            className="px-1 rounded text-slate-100"
          >
            {h.sentence}{" "}
          </span>
        ))}
      </p>

      <div className="mt-5 flex items-center gap-4 text-[10px] text-slate-500">
        <span className="flex items-center gap-2">
          <span className="inline-block w-8 h-2 rounded"
                style={{ background: "rgba(248,113,113,0.55)" }} />
          predictable
        </span>
        <span className="flex items-center gap-2">
          <span className="inline-block w-8 h-2 rounded bg-slate-800" />
          variable
        </span>
      </div>

      {(matched.length > 0 || hedges.length > 0) && (
        <div className="mt-5 pt-4 border-t border-slate-800 space-y-4">
          {matched.length > 0 && (
            <div>
              <div className="text-[10px] uppercase text-slate-500 mb-2">
                ai-phrase matches ({matched.length})
              </div>
              <div className="flex flex-wrap gap-2">
                {matched.map((m, i) => (
                  <span key={i}
                        className="text-[11px] px-2 py-0.5 rounded
                                   bg-red-500/10 border border-red-500/30
                                   text-red-300">
                    {m}
                  </span>
                ))}
              </div>
            </div>
          )}
          {hedges.length > 0 && (
            <div>
              <div className="text-[10px] uppercase text-slate-500 mb-2">
                hedges ({hedges.length})
              </div>
              <div className="flex flex-wrap gap-2">
                {hedges.map((h, i) => (
                  <span key={i}
                        className="text-[11px] px-2 py-0.5 rounded
                                   bg-amber-500/10 border border-amber-500/30
                                   text-amber-300">
                    {h}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
