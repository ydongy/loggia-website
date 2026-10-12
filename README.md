# Loggia website

[![CI](https://github.com/ydongy/loggia-website/actions/workflows/ci.yml/badge.svg)](https://github.com/ydongy/loggia-website/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Static website of Loggia (`https://useloggia.com`), nine languages, deployed as Cloudflare Workers static assets
from `public/`. No framework and no build step on deploy: pages are generated locally from `i18n/*.json` and
`changelog.json` with Python (standard library only), and the generated files are committed.

## Quick start

Python 3 only (standard library); no install step.

```
git clone https://github.com/ydongy/loggia-website.git
cd loggia-website
python3 scripts/sitekit/preview.py      # preview at http://127.0.0.1:8765
```

## Deploy

Cloudflare Workers static assets, project `loggia`; `wrangler.jsonc` serves `public/`.

- Dashboard (Workers & Pages > Create > Connect to Git): project name `loggia`, production branch `main`,
  build command empty, deploy command `npx wrangler deploy`.
- The custom domain `useloggia.com` is bound in the dashboard (project > Domains), not in the config.
  `workers_dev` and `preview_urls` are off on purpose. If the project is re-created or reconnected, bind the
  domain again: without it the site is unreachable (on 2026-10-10 the root domain had no DNS record until it
  was added back).
- The Workers Builds check that matters is the one on `main`. On pull-request branches it has reported
  failure on every pull request so far, including ones that were merged and deployed fine.
- `public/_headers` sets the Content-Security-Policy and two other headers; update it if the feed address
  changes (`docs/adr/0004-content-security-policy.md`). It allows the script of Cloudflare Web Analytics, the
  only analytics on the site (`docs/adr/0008-cloudflare-web-analytics.md`).
- Support mail `support@useloggia.com` is forwarded by Cloudflare Email Routing (dashboard > Email > Email
  Routing).

## Development

```
python3 scripts/sitekit/check_i18n.py   # every language against English
python3 scripts/build.py                # generate every page into public/
git diff --exit-code public/            # the committed output matches the sources
python3 scripts/sitekit/check_site.py   # pages, links, anchors, CSP
python3 scripts/check_facts.py          # facts agree across languages
python3 scripts/sitekit/preview.py      # preview at http://127.0.0.1:8765
```

- Edit the copy in `i18n/<code>.json`, never the generated HTML. Commit generated files together with the
  source change that produces them.
- Page structure, checks and the preview server are ydongy's `sitekit`, vendored in
  `scripts/sitekit/` (the version is in `scripts/sitekit/VERSION`; `docs/adr/0005-vendored-sitekit.md`).
  `scripts/build.py` holds the Loggia settings and the home page; styles are in `public/style.css`
  (`docs/design.md`).
- Preview with `scripts/sitekit/preview.py` or `npx wrangler dev`, not `python3 -m http.server`: only those
  serve extensionless paths such as `/zh/privacy` the way production does.
- Share image: `public/og.png` (1200x630) is rendered from `design/og.html` by `scripts/export-og.sh`
  (headless Chrome); render it again when the icon or the tagline changes.

## Pages

| Page | Address | Source of its copy |
|---|---|---|
| Home | `/` | `home` in the language file; sections `#download` and `#pricing` |
| FAQ | `/faq` | `faq` |
| Terms of Service | `/terms` | `terms` |
| Privacy Policy | `/privacy` | `privacy` |
| Refund Policy | `/refund` | `refund` |
| Changelog | `/changelog` | `changelog.json` |
| Not found | `404.html` | `not_found()` in the generator |

Each language lives under its own path (English at `/`, Simplified Chinese at `/zh/`). Every page has exactly
one address; there are no redirects or aliases (`docs/adr/0003-one-address-per-page.md`).

## Languages

`en`, `zh`, `zh-hant`, `ja`, `ko`, `fr`, `de`, `es`, `pt`. To add a language (see [CONTRIBUTING.md](CONTRIBUTING.md) first; open an issue), English
(`i18n/en.json`) is the reference and the others follow its structure. A language is a line in
`i18n/languages.json` (path, HTML `lang`, browser language prefixes for the first-visit redirect in `lang.js`),
`i18n/<code>.json`, and five pairs of screenshots `public/img/app-<code>-<scene>-{light,dark}.webp`
(`docs/adr/0006-screenshot-carousel.md`).

## Content sources

Page by page, where the text is decided: `docs/content.md`. In short:

- Facts (plan limits, price, refund window, offline grace) come from the product's own facts list and are
  mirrored in the Facts table of `docs/content.md`, which `scripts/check_facts.py` reads.
- The Terms of Service are the app's license text, translated section for section.
- `changelog.json` is written by Loggia's release tooling, which opens a pull request against this repository
  for each release. Do not edit it by hand, and keep its path and format (`docs/contracts.md`).
- Screenshots are exported from the app; rename `zh-Hans` to `zh`, `zh-Hant` to `zh-hant` and `pt-BR` to `pt`
  when copying.

## App dependencies

The app links to these addresses in the visitor's language (English has no prefix) and they stay stable:
`/privacy`, `/terms`, `/refund`, `/changelog`, and the home page sections `/#download` and `/#pricing`. The
download button reads `https://dl.useloggia.com/latest.json` (version and checksum, written by the app's
release tooling; the bucket allows CORS from `https://useloggia.com`). The app's own updates do not touch this
site: Sparkle reads `https://dl.useloggia.com/appcast.xml`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): copy lives in `i18n/*.json`; after editing run `python3 scripts/build.py` and
commit the regenerated `public/` with the change.

## License

The source code in this repository is released under the [MIT License](LICENSE).

The Loggia name, logo and icon, and the website copy (text and translations), are copyright (c) 2026 ydongy and are not covered by the MIT License. Loggia is a closed-source product (only this website is open); the name and icon may not be used to suggest endorsement or to name a derived work. 品牌名称、Logo、图标与网站文案版权归 ydongy 所有，不在 MIT 授权范围内。
