import { useState } from "react";
import DropZone from "./components/DropZone";
import SyntheticMeter from "./components/SyntheticMeter";
import HeatmapOverlay from "./components/HeatmapOverlay";
import ComparisonPane from "./components/ComparisonPane";
import ArtifactPanel from "./components/ArtifactPanel";
import ReportButton from "./components/ReportButton";
import SmokingGun from "./components/SmokingGun";
import { useAnalyze } from "./hooks/useAnalyze";

export default function App() {
  const { result, loading, error, run } = useAnalyze();
  const [baseline, setBaseline] = useState("");

  function handleInput({ file, text }) {
    run({ file, text, humanBaseline: baseline });
  }

  return (
    <div className="min-h-screen">
      <Header />

      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6 px-6 lg:px-10 py-8 max-w-[1400px] mx-auto">
        <section className="lg:col-span-2 space-y-6">
          <DropZone onSubmit={handleInput} loading={loading} />

          {error && (
            <div className="panel border-red-500/40 text-red-300 text-sm">
              ⚠ {error}
            </div>
          )}

          {result && (
            <>
              <SmokingGun
                smokingGun={result.smoking_gun}
                modality={result.analyzed_modality}
                layers={result.layers_triggered}
              />
              <HeatmapOverlay
                heatmap={result.heatmap}
                matched={result.matched_phrases}
                hedges={result.hedge_phrases}
              />
              {result.artifacts && (
                <ArtifactPanel artifacts={result.artifacts} />
              )}
            </>
          )}

          {!result && !loading && !error && <PlaceholderDashboard />}
        </section>

        <aside className="space-y-6">
          <SyntheticMeter
            probability={result?.ai_probability ?? 0}
            score={result?.predictive_confidence_score}
            components={result?.components}
            verdict={result?.final_verdict ?? result?.verdict}
          />
          <ComparisonPane value={baseline} onChange={setBaseline} />
          {result && <ReportButton result={result} />}
        </aside>
      </main>

      <Footer />
    </div>
  );
}

function Header() {
  return (
    <header className="border-b border-cyan-500/20 backdrop-blur-sm
                       bg-forensic-bg/80 sticky top-0 z-10">
      <div className="max-w-[1400px] mx-auto px-6 lg:px-10 py-5
                      flex items-center justify-between">
        <div>
          <h1 className="text-lg tracking-wide text-cyan-400">
            ai text detector
          </h1>
          <p className="text-[10px] text-slate-500">
            7-layer ensemble · sentence-transformer embeddings
          </p>
        </div>
        <div className="text-[10px] text-slate-500">v0.4</div>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="border-t border-slate-800/50 mt-12 py-4 text-center
                       text-[10px] text-slate-600">
      a personal project · github.com/faheem
    </footer>
  );
}

function PlaceholderDashboard() {
  return (
    <div className="panel text-center py-16 text-slate-500">
      <div className="text-sm">waiting for input</div>
      <div className="text-[10px] mt-2 text-slate-600">
        drop a file or paste text above to start
      </div>
    </div>
  );
}
