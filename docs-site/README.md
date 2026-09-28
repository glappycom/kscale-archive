# Recovered websites

Wayback Machine copies of the public K-Scale sites, taken from `meta/KSCALE-DEV-WAYBACK-SNAPSHOTS.csv` on 28 September 2026. Each page was requested as an `id_` URL (`https://web.archive.org/web/<timestamp>id_/<original>`), which returns the archived document without the Wayback toolbar.

205 URLs were attempted. 200 were saved. 5 failed and are marked `error` in `manifest.csv`:

- `http://api.kscale.dev/` — Wayback 404
- `http://notion.kscale.dev/` — Wayback 404
- `http://media.kscale.dev/` — empty body
- `https://blog.kscale.dev/_/graphql` — HTTP 403
- `https://blog.kscale.dev/efficient-vision-language-action-models-82b4607de39d` — HTTP 403

`docs.kscale.dev` (148 pages) and `kscale.dev` (23 pages) were all saved.

Alongside the HTML, pages that contained article text were converted to Markdown (`index.md` next to `index.html`). 96 pages had a real article. 55 later `docs.kscale.dev` captures are the ReadMe.io JavaScript shell: the HTML is preserved, and the Markdown file says the article body was not in the archived HTML. Older pages (build guides, components, bill of materials, CAD, print guide) still have their text.

Images and other fetched media are under `_assets/`. A production `secretKey` that ReadMe had embedded in a few page shells was replaced with `[REDACTED]` before this mirror was published.

`manifest.csv` lists every URL, the timestamp used, the HTTP status, and the file that was written.
