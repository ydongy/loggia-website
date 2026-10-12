<!-- template: website/README.md v1 -->
# Loggia website

Static website of Loggia (`https://useloggia.com`), nine languages, deployed as Cloudflare Workers static assets
from `public/`. No framework and no build step on deploy: pages are generated locally from `i18n/*.json` and
`changelog.json` with Python (standard library only), and the generated files are committed.

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

## Work on it

```
python3 scripts/sitekit/check_i18n.py   # every language against English
python3 scripts/build.py                # generate every page into public/
git diff --exit-code public/            # the committed output matches the sources
python3 scripts/sitekit/check_site.py   # pages, links, anchors, CSP
python3 scripts/check_facts.py          # facts agree across languages
python3 scripts/sitekit/preview.py      # preview at http://127.0.0.1:8787
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
- Documents are checked against ydongy's templates:
  `python3 <.github repository>/scripts/check-docs.py .` (CI runs it in `.github/workflows/docs.yml`).

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

`en`, `zh`, `zh-hant`, `ja`, `ko`, `fr`, `de`, `es`, `pt`. The rules and the steps to add a language are in the
ydongy handbook (`https://github.com/ydongy/.github/tree/6b48552c969c28a954498123bb502a556f8eed79/handbook`):
`handbook/guides/localization.md` and `handbook/types/app/playbooks/add-language.md`. In this repository a language is a line in
`i18n/languages.json` (path, HTML `lang`, browser language prefixes for the first-visit redirect in `lang.js`),
`i18n/<code>.json`, and five pairs of screenshots `public/img/app-<code>-<scene>-{light,dark}.webp`
(`docs/adr/0006-screenshot-carousel.md`).

## Content sources

Page by page, where the text is decided: `docs/content.md`. In short:

- Facts (plan limits, price, refund window, offline grace) come from the app repository's facts table
  (https://github.com/ydongy/loggia/blob/main/docs/legal.md#facts-that-must-match-the-code) and are
  mirrored in the Facts table of `docs/content.md`, which `scripts/check_facts.py` reads.
- The Terms of Service are the app's `LICENSE`, translated section for section.
- `changelog.json` is written by the app's `scripts/website-changelog.py` from the app's `CHANGELOG.md` and
  `CHANGELOG.zh.md`; `scripts/build.py` runs the full build afterwards. Never edit it by hand.
- Screenshots are exported by the app's `scripts/export-website-shots.sh`; rename `zh-Hans` to `zh`, `zh-Hant`
  to `zh-hant` and `pt-BR` to `pt` when copying.

## App dependencies

The app links to these addresses in the visitor's language (English has no prefix) and they stay stable:
`/privacy`, `/terms`, `/refund`, `/changelog`, and the home page sections `/#download` and `/#pricing`. The
download button reads `https://dl.useloggia.com/latest.json` (version and checksum, written by the app's
release script; the bucket allows CORS from `https://useloggia.com`). The app's own updates do not touch this
site: Sparkle reads `https://dl.useloggia.com/appcast.xml`. The app's side of the contract is the website document in the app repository.

## License

The source code in this repository is released under the [MIT License](LICENSE).

The Loggia name, logo and icon, and the website copy (text and translations), are copyright (c) 2026 ydongy and are not covered by the MIT License. Loggia is a closed-source product; the name and icon may not be used to suggest endorsement or to name a derived work. 品牌名称、Logo、图标与网站文案版权归 ydongy 所有，不在 MIT 授权范围内。
