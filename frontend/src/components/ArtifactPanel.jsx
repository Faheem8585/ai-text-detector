export default function ArtifactPanel({ artifacts }) {
  if (!artifacts) return null;
  const { flags, melting_glyphs = 0, kerning_anomalies, glyph_noise,
          impossible_signage = [], score } = artifacts;

  return (
    <div className="panel">
      <div className="panel-title">ocr artifacts</div>

      <div className="grid grid-cols-4 gap-3 text-center">
        <Stat label="melting" v={melting_glyphs} />
        <Stat label="kerning" v={kerning_anomalies} />
        <Stat label="glyphs" v={glyph_noise} />
        <Stat label="score" v={`${Math.round(score * 100)}%`} highlight />
      </div>

      {impossible_signage.length > 0 && (
        <div className="mt-4 p-3 rounded-lg border border-red-500/30 bg-red-500/5">
          <div className="text-[10px] uppercase text-red-300 mb-1">
            impossible signage
          </div>
          <div className="flex flex-wrap gap-1.5">
            {impossible_signage.map((t, i) => (
              <code key={i} className="text-[11px] px-2 py-0.5 rounded
                                       bg-red-500/15 border border-red-500/40
                                       text-red-200">{t}</code>
            ))}
          </div>
        </div>
      )}

      {flags.length > 0 ? (
        <div className="mt-4">
          <div className="text-[10px] uppercase tracking-[0.3em] text-slate-500 mb-2">
            Flagged Tokens
          </div>
          <div className="flex flex-wrap gap-1.5">
            {flags.map((f, i) => (
              <code key={i}
                    className="text-[11px] px-2 py-0.5 rounded
                               bg-amber-500/10 border border-amber-500/30
                               text-amber-300">
                {f}
              </code>
            ))}
          </div>
        </div>
      ) : (
        <div className="mt-4 text-[11px] text-slate-500">
          no artifacts detected
        </div>
      )}
    </div>
  );
}

function Stat({ label, v, highlight }) {
  return (
    <div className={`rounded-lg border p-3
      ${highlight ? "border-cyan-500/40 bg-cyan-500/5"
                  : "border-slate-800 bg-slate-950/40"}`}>
      <div className={`text-xl font-bold tabular-nums
        ${highlight ? "text-cyan-300" : "text-slate-200"}`}>{v}</div>
      <div className="text-[10px] text-slate-500">
        {label}
      </div>
    </div>
  );
}
