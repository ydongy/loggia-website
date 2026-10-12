# Contributing

Thanks for helping with the Loggia website. For anything larger than a typo or a one-line fix, open an issue first so
we can agree on the approach.

## Setup

Python 3 is all you need (standard library only; no Node, no pip install). `npx wrangler dev` is optional.

```
git clone https://github.com/ydongy/loggia-website.git
cd loggia-website
python3 scripts/sitekit/preview.py      # preview; prints the local address
```

Use the preview script or `npx wrangler dev`, not `python3 -m http.server`: only those serve extensionless paths
such as `/zh/privacy` the way production does.

## Changing text

All page text lives in `i18n/<code>.json`. The HTML in `public/` is generated and committed, because the
site is deployed straight from the repository with no build step.

1. Edit `i18n/en.json` first (English is the reference), then the same place in every other language file.
2. Run the checks below. `python3 scripts/build.py` regenerates `public/`.
3. Commit `i18n/` and the regenerated `public/` together. CI fails with "public/ is stale" otherwise.

Never edit generated HTML in `public/` by hand, and never edit `scripts/sitekit/` (a vendored copy of
[sitekit](https://github.com/ydongy/sitekit); changes belong there).

## Translations

- Fixing a wording problem in a language: edit `i18n/<code>.json`, rebuild, send a pull request. Say in the
  description why the new wording is better.
- Adding a language: add it to `i18n/languages.json`, translate `i18n/en.json` into `i18n/<code>.json` with the
  same structure, tags, links and placeholders, and the same JSON formatting (2 spaces, UTF-8, trailing newline).
  Open an issue first; new languages also need translated assets where the README says so.
- No em or en dashes in the copy. Legal pages and the FAQ keep the note that the English text is the reference.
- Numbers in legal text are facts checked by `scripts/check_facts.py` against `docs/content.md`; do not change
  them in a translation PR.

## Checks

CI runs these; run them before you push:

```
python3 scripts/sitekit/check_i18n.py   # every language against English
python3 scripts/build.py                # regenerate public/
git diff --exit-code public/            # the committed output matches the sources
python3 scripts/sitekit/check_site.py   # pages, links, anchors, Content-Security-Policy
python3 scripts/check_facts.py          # facts agree across languages
```

## Commits, branches and pull requests

- Conventional Commits for commit messages and PR titles:
  `feat|fix|docs|refactor|perf|test|build|ci|chore|revert(scope)!: subject`. Scopes are listed in
  [docs/contracts.md](docs/contracts.md).
- Branch name `<type>/<issue>-<slug>`, for example `fix/12-refund-wording`.
- The maintainer squash-merges. No sign-off is required.
- Do not edit `changelog.json` by hand; the release tooling writes it. Add website changes to `CHANGELOG.md` under
  `## [Unreleased]`.

## License

By contributing you agree that your code contributions are released under the [MIT License](LICENSE). The product
name, logo, icon and the site copy are not covered by it (see the README).
