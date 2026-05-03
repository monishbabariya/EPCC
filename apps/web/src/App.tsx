import { useQuery } from "@tanstack/react-query";

interface Health {
  status: string;
  env: string;
  version: string;
}

async function fetchHealth(): Promise<Health> {
  const res = await fetch("/api/v1/health");
  if (!res.ok) {
    throw new Error(`Health check failed: ${res.status}`);
  }
  return res.json();
}

export function App() {
  const { data, error, isLoading } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
  });

  return (
    <main className="min-h-screen bg-slate-50 p-8 font-sans text-slate-900">
      <div className="mx-auto max-w-2xl">
        <h1 className="mb-2 text-3xl font-bold">EPCC</h1>
        <p className="mb-8 text-slate-600">
          Enterprise Project Management — Round 25 scaffold. Modules land Round 27+.
        </p>
        <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-2 text-lg font-semibold">Backend health</h2>
          {isLoading && <p className="text-slate-500">Checking…</p>}
          {error instanceof Error && (
            <p className="text-red-600">Unable to reach API: {error.message}</p>
          )}
          {data && (
            <dl className="grid grid-cols-2 gap-2 text-sm">
              <dt className="font-medium text-slate-500">Status</dt>
              <dd className="font-mono">{data.status}</dd>
              <dt className="font-medium text-slate-500">Env</dt>
              <dd className="font-mono">{data.env}</dd>
              <dt className="font-medium text-slate-500">Version</dt>
              <dd className="font-mono">{data.version}</dd>
            </dl>
          )}
        </section>
      </div>
    </main>
  );
}
