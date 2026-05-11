import { useRef, useState } from "react";

const ACCEPT = ".txt,.pdf,.png,.jpg,.jpeg,.webp";

export default function DropZone({ onSubmit, loading }) {
  const [text, setText] = useState("");
  const [drag, setDrag] = useState(false);
  const [fileName, setFileName] = useState("");
  const inputRef = useRef(null);

  function pickFile(file) {
    if (!file) return;
    setFileName(file.name);
    onSubmit({ file });
  }

  function onDrop(e) {
    e.preventDefault();
    setDrag(false);
    pickFile(e.dataTransfer.files?.[0]);
  }

  return (
    <div className="panel relative overflow-hidden">
      <div className="panel-title">input</div>

      <div
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative cursor-pointer border-2 border-dashed rounded-xl
          p-8 text-center transition overflow-hidden
          ${drag ? "border-cyan-400 bg-cyan-500/5"
                 : "border-slate-700 hover:border-cyan-500/60"}`}
      >
        <div className="text-cyan-400 text-sm">
          drop a file here
        </div>
        <div className="text-[10px] text-slate-500 mt-2">
          .txt, .pdf, .png, .jpg, .webp · 10 MB max
        </div>
        {fileName && (
          <div className="mt-3 text-xs text-emerald-400 truncate">
            {fileName}
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPT}
          className="hidden"
          onChange={(e) => pickFile(e.target.files?.[0])}
        />
      </div>

      <div className="mt-4">
        <label className="text-[10px] text-slate-500">
          or paste text
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="paste 100+ words for a reliable score"
          className="mt-2 w-full h-40 bg-slate-950/60 border border-slate-800
                     rounded-lg p-3 text-sm focus:border-cyan-500
                     focus:outline-none focus:ring-1 focus:ring-cyan-500/30
                     placeholder:text-slate-600"
        />
        <button
          disabled={loading || !text.trim()}
          onClick={() => onSubmit({ text })}
          className="btn-cyber mt-3 w-full"
        >
          {loading ? "analyzing..." : "analyze"}
        </button>
      </div>
    </div>
  );
}
