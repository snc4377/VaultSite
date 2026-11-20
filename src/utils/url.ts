/**
 * GitHub Pages serves project sites from `/<repo>/`, so every root-absolute
 * link has to carry Astro's `base` prefix. In dev and on a custom domain
 * BASE_URL is "/" and these helpers are a no-op.
 */
const raw = import.meta.env.BASE_URL;
const base = raw.replace(/\/+$/, "");

export function withBase(path: string): string {
  const clean = path.startsWith("/") ? path : `/${path}`;
  return `${base}${clean}` || "/";
}
