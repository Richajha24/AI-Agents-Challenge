import Link from "next/link";

export default function Page() {
    return (
        <main className="min-h-screen p-6">
            <div className="mx-auto max-w-5xl">
                <header className="mb-6">
                    <div className="card rounded-2xl p-6">
                        <h1 className="text-2xl font-semibold tracking-tight">Executive Assistant</h1>
                        <p className="mt-2 text-sm text-white/70">
                            Priority analysis, meeting briefs, decision support, and workspace report orchestration.
                        </p>
                    </div>
                </header>

                <section className="grid gap-4 md:grid-cols-2">
                    <div className="card rounded-2xl p-5">
                        <h2 className="text-lg font-semibold">Workspace Report</h2>
                        <p className="mt-1 text-sm text-white/70">Generate a full report in background with progress.</p>
                        <Link
                            href="/workspace"
                            className="mt-4 inline-flex items-center rounded-xl border border-gold/40 bg-gold/10 px-3 py-2 text-sm font-medium text-ivory hover:bg-gold/20"
                        >
                            Open
                        </Link>
                    </div>

                    <div className="card rounded-2xl p-5">
                        <h2 className="text-lg font-semibold">Priority Tasks</h2>
                        <p className="mt-1 text-sm text-white/70">Rank tasks, suggest focus, and build critical path.</p>
                        <Link
                            href="/tasks"
                            className="mt-4 inline-flex items-center rounded-xl border border-gold/40 bg-gold/10 px-3 py-2 text-sm font-medium text-ivory hover:bg-gold/20"
                        >
                            Open
                        </Link>
                    </div>

                    <div className="card rounded-2xl p-5">
                        <h2 className="text-lg font-semibold">Meeting Preparation</h2>
                        <p className="mt-1 text-sm text-white/70">Agenda, discussion points, and risk areas.</p>
                        <Link
                            href="/meetings"
                            className="mt-4 inline-flex items-center rounded-xl border border-gold/40 bg-gold/10 px-3 py-2 text-sm font-medium text-ivory hover:bg-gold/20"
                        >
                            Open
                        </Link>
                    </div>

                    <div className="card rounded-2xl p-5">
                        <h2 className="text-lg font-semibold">Decision Support</h2>
                        <p className="mt-1 text-sm text-white/70">Pros/cons, risk analysis, and recommendation.</p>
                        <Link
                            href="/decisions"
                            className="mt-4 inline-flex items-center rounded-xl border border-gold/40 bg-gold/10 px-3 py-2 text-sm font-medium text-ivory hover:bg-gold/20"
                        >
                            Open
                        </Link>
                    </div>
                </section>
            </div>
        </main>
    );
}

