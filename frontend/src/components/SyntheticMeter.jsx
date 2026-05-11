import { useEffect, useState } from "react";

const LABELS = {
  centroid_tightness:        ["centroid tightness",   "23%"],
  semantic_drift:            ["semantic drift",       "22%"],
  hedge_density:             ["hedge frequency",      "15%"],
  ai_phrase_frequency:       ["ai-phrase patterns",   "12%"],
  structural_symmetry:       ["structural symmetry",  "12%"],
  linguistic_predictability: ["predictability",       "8%"],
  sentence_variance:         ["sentence variance",    "8%"],
};

const ORDER = [
  "centroid_tightness", "semantic_drift", "hedge_density",
  "ai_phrase_frequency", "structural_symmetry",
  "linguistic_predictability", "sentence_variance",
];

export default function SyntheticMeter({ probability = 0, components, verdict, score }) {
  const target = Math.max(0, Math.min(1, probability));
  const [v, setV] = useState(0);

  useEffect(() => {
    let raf, start;
    const from = v;
    const dur = 700;
    function tick(t) {
      if (!start) start = t;
      const k = Math.min(1, (t - start) / dur);
      const eased = 1 - Math.pow(1 - k, 3);
      setV(from + (target - from) * eased);
      if (k < 1) raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target]);

  const pct = score != null ? score : Math.round(v * 100);
  const tone =
    pct > 80 ? { ring: "#dc2626", text: "text-red-500" }
    : pct > 55 ? { ring: "#f87171", text: "text-red-400" }
    : pct > 30 ? { ring: "#fbbf24", text: "text-amber-400" }
    : { ring: "#34d399", text: "text-emerald-400" };

  const ARC = 264;
  const dash = v * ARC;

  return (
    <div className="panel">
      <div className="panel-title">score</div>
      <div className="relative h-48 w-48 mx-auto">
        <svg viewBox="0 0 100 100" className="absolute inset-0">
          <circle cx="50" cy="50" r="42" stroke="#1e293b"
                  strokeWidth="8" fill="none"
                  strokeDasharray={`${ARC} 999`}
                  transform="rotate(135 50 50)" strokeLinecap="round" />
          <circle cx="50" cy="50" r="42" fill="none"
                  stroke={tone.ring} strokeWidth="8" strokeLinecap="round"
                  strokeDasharray={`${dash} 999`}
                  transform="rotate(135 50 50)"
                  style={{ filter: `drop-shadow(0 0 6px ${tone.ring})` }} />
          {[...Array(28)].map((_, i) => {
            const a = (135 + (i / 27) * 270) * (Math.PI / 180);
            const x1 = 50 + Math.cos(a) * 48;
            const y1 = 50 + Math.sin(a) * 48;
            const x2 = 50 + Math.cos(a) * 50;
            const y2 = 50 + Math.sin(a) * 50;
            return (
              <line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
                    stroke="#334155" strokeWidth="0.6" />
            );
          })}
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-5xl font-bold tabular-nums ${tone.text}`}>
            {pct}
            <span className="text-2xl text-slate-500">%</span>
          </span>
          <span className="text-[10px] text-slate-500 mt-1">
            ai probability
          </span>
        </div>
      </div>

      {verdict && (
        <div className={`mt-4 text-center text-xs ${tone.text}`}>
          {verdict.toLowerCase()}
        </div>
      )}

      {components && (
        <ul className="mt-5 space-y-2 text-[11px]">
          {ORDER.map((key) => (
            <Bar key={key}
                 label={LABELS[key][0]}
                 w={LABELS[key][1]}
                 v={components[key]} />
          ))}
        </ul>
      )}
    </div>
  );
}

function Bar({ label, w, v }) {
  return (
    <li>
      <div className="flex justify-between text-slate-400">
        <span>{label} <span className="text-slate-600">({w})</span></span>
        <span className="text-cyan-300 tabular-nums">{(v * 100).toFixed(1)}%</span>
      </div>
      <div className="h-1 mt-1 rounded bg-slate-800 overflow-hidden">
        <div className={`h-full bg-gradient-to-r
          ${v > 0.55 ? "from-red-500 to-red-300"
                     : "from-cyan-500 to-cyan-300"}`}
             style={{ width: `${v * 100}%` }} />
      </div>
    </li>
  );
}
