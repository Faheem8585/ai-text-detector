export default function SmokingGun({ smokingGun, modality, layers = [] }) {
  if (!smokingGun?.quote && !layers.length) return null;

  return (
    <div className="panel border-red-500/25 bg-red-950/10">
      <div className="panel-title text-red-400/80">
        <span>key evidence</span>
      </div>

      <div className="flex justify-between items-start mb-3 text-[10px] text-slate-500">
        <span>modality: <span className="text-cyan-300">{modality}</span></span>
        <span>{layers.length} layer{layers.length === 1 ? "" : "s"} triggered</span>
      </div>

      {smokingGun?.quote ? (
        <blockquote className="border-l-2 border-red-500/60 pl-4 py-1 my-2">
          <p className="text-sm italic text-slate-100 leading-relaxed">
            "{smokingGun.quote}"
          </p>
          <p className="text-[11px] text-red-300/80 mt-2">
            {smokingGun.reason}
          </p>
        </blockquote>
      ) : (
        <p className="text-xs text-slate-500 italic">
          No isolating excerpt — verdict driven by aggregate signals.
        </p>
      )}

      {layers.length > 0 && (
        <div className="mt-4 pt-3 border-t border-slate-800">
          <div className="text-[10px] uppercase text-slate-500 mb-2">
            layers triggered
          </div>
          <div className="flex flex-wrap gap-2">
            {layers.map((l, i) => (
              <span key={i}
                    className="text-[11px] px-2 py-1 rounded
                               bg-cyan-500/10 border border-cyan-500/30
                               text-cyan-300">
                {l}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
