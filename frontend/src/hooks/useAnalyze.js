import { useState } from "react";
import { analyze } from "../lib/api";

export function useAnalyze() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function run({ file, text, humanBaseline }) {
    setLoading(true);
    setError(null);
    try {
      const out = await analyze({ file, text, humanBaseline });
      setResult(out);
      return out;
    } catch (e) {
      setError(e.message);
      setResult(null);
      return null;
    } finally {
      setLoading(false);
    }
  }

  return { result, loading, error, run, reset: () => setResult(null) };
}
