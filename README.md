# Vibe Apps

Small browser tools by Max Pog, served at https://maxpog.com via GitHub Pages
(public repo `pogumax/vibe-apps`, branch `main`, folder `docs/`).

| Page | Folder | URL |
|---|---|---|
| Personal page | `home/` | https://maxpog.com/ |
| Don't Stop Writing | `nonstop/` | https://maxpog.com/nonstop/ |

## How it works

- Each app is `<app>/index.html`, a page fragment with a `<!-- body -->` marker. The same file
  is also published as a Claude artifact.
- `python3 build.py` wraps every fragment into a full HTML page in `docs/` (`home/` becomes the
  site root) and writes `docs/CNAME`.
- Commit and push `main`: GitHub Pages redeploys in about a minute.

## DNS (Namecheap, maxpog.com → Advanced DNS)

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` |
| CNAME | `www` | `pogumax.github.io.` |

Everything is static and runs in the visitor's browser: no server, no database. Texts stay in
the visitor's own browser storage.
