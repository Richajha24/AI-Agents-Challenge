"use client";

import { useEffect, useState } from "react";
import { analyzeDecision, getDecisionHistory } from "@/lib/api";

export default function DecisionsPage() {
    const [problem, setProblem] = useState<string>("Which cloud platform should we standardize on for new services?");
    const [optionsRaw, setOptionsRaw] = useState<string>("AWS
GCP
Azure");

  const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<any | null>(null);

    const [history, setHistory] = useState<any[]>([]);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [historyError, setHistoryError] = useState<string | null>(null);

    const options = optionsRaw
        .split("\n")
        .map((o) => o.trim())
        .filter(Boolean);

    async function onAnalyze() {
        setLoading(true);
        setError(null);
        try {
            const res = await analyzeDecision({ problem_statement: problem, options });
            setResult(res);
        } catch (e: any) {
            setError(e?.message || "Failed to analyze decision");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        (async () => {
            setHistoryLoading(true);
            setHistoryError(null);
            try {
                const items = await getDecisionHistory(20);
                setHistory(items);
            } catch (e: any) {
                setHistoryError(e?.message || "Failed to load decision history");
            } finally {
                setHistoryLoading(false);
            }
        })();
    }, []);

    return (
        <main className="min-h-screen p-6">
            <div className="mx-auto w-full max-w-5xl">
                <div className="card rounded-2xl p-6">
                    <h1 className="text-xl font-semibold">Decision Support</h1>
                    <p className="mt-1 text-sm text-white/70">Compare options with pros/cons, risk analysis, and a recommendation.</p>

                    <div className="mt-6 grid gap-4 md:grid-cols-2">
                        <label className="block md:col-span-2">
                            <span className="text-sm text-white/80">Problem statement</span>
                            <textarea
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                rows={4}
                                value={problem}
                                onChange={(e) => setProblem(e.target.value)}
                            />
                        </label>

                        <label className="block md:col-span-2">
                            <span className="text-sm text-white/80">Options (one per line)</span>
                            <textarea
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                rows={5}
                                value={optionsRaw}
                                onChange={(e) => setOptionsRaw(e.target.value)}
                            />
                        </label>
                    </div>

                    <div className="mt-6 flex items-center gap-3">
                        <button
                            onClick={onAnalyze}
                            disabled={loading}
                            className="rounded-xl bg-gold/20 px-4 py-2 text-sm font-semibold text-ivory ring-1 ring-gold/40 hover:bg-gold/30 disabled:opacity-50"
                        >
                            {loading ? "Analyzing..." : "Analyze Decision"}
                        </button>
                    </div>

                    {error ? <div className="mt-4 rounded-xl border border-red-400/30 bg-red-400/10 p-3 text-sm">{error}</div> : null}
                </div>

                {result ? (
                    <section className="mt-6 card rounded-2xl p-6">
                        <h2 className="text-lg font-semibold">Analysis</h2>

                        <div className="mt-4 grid gap-4 md:grid-cols-2">
                            <div>
                                <h3 className="text-sm font-semibold">Decision Framework</h3>
                                <p className="mt-2 text-xs text-white/75">{result?.decision_framework}</p>
                            </div>

                            <div>
                                <h3 className="text-sm font-semibold">Recommendation</h3>
                                <p className="mt-2 text-xs text-white/75">{result?.recommendation}</p>
                            </div>
                        </div>

                        <div className="mt-6">
                            <h3 className="text-sm font-semibold">Pros & Cons</h3>
                            <div className="mt-3 grid gap-4 md:grid-cols-1">
                                {Object.entries(result?.pros_and_cons || {}).map(([option, pc]: any) => (
                                    <div key={option} className="rounded-xl border border-gold/20 bg-graphite/30 p-4">
                                        <div className="text-sm font-semibold text-ivory">{option}</div>
                                        <pre className="mt-2 whitespace-pre-wrap text-xs text-white/75">{JSON.stringify(pc, null, 2)}</pre>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="mt-6">
                            <h3 className="text-sm font-semibold">Risk Analysis</h3>
                            <pre className="mt-2 whitespace-pre-wrap text-xs text-white/75">{JSON.stringify(result?.risk_analysis, null, 2)}</pre>
                        </div>
                    </section>
                ) : null}

                <section className="mt-6">
                    <div className="card rounded-2xl p-6">
                        <h2 className="text-lg font-semibold">Decision History</h2>
                        {historyError ? <div className="mt-2 text-sm text-red-300">{historyError}</div> : null}
                        {historyLoading ? <div className="mt-2 text-sm text-white/70">Loading...</div> : null}

                        <div className="mt-4 space-y-3">
                            {history.slice(0, 10).map((h) => (
                                <div key={h.decision_id} className="rounded-xl border border-gold/20 bg-graphite/30 p-4">
                                    <div className="flex items-start justify-between gap-3">
                                        <div>
                                            <div className="text-sm font-semibold text-ivory">{h.problem_statement}</div>
                                            <div className="mt-1 text-xs text-white/60">{new Date(h.created_at).toLocaleString()}</div>
                                        </div>
                                    </div>
                                    <div className="mt-2 text-xs text-white/70">Options: {(h.options || []).join(", ")}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            </div>
        </main>
    );
}


