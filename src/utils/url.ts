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

/**
 * Inverse of withBase: Astro.url.pathname carries the base prefix
 * ("/VaultSite/blog/"), but nav hrefs are root-relative ("/blog"), so the
 * active-route comparison has to strip it first.
 */
export function stripBase(pathname: string): string {
  const clean = pathname.replace(/\/+$/, "") || "/";
  if (base && (clean === base || clean.startsWith(`${base}/`))) {
    return clean.slice(base.length) || "/";
  }
  return clean;
}
