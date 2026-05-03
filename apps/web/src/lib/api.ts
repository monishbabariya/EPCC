/**
 * Typed API client.
 *
 * Round 25 scaffold: thin wrapper. Once `@epcc/api-types` is generated
 * (Round 26), swap to `createClient<paths>()` from openapi-fetch.
 */

const baseUrl = import.meta.env["VITE_API_BASE_URL"] ?? "/api/v1";

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${baseUrl}${path}`);
  if (!res.ok) {
    throw new Error(`GET ${path} failed: ${res.status}`);
  }
  return (await res.json()) as T;
}
