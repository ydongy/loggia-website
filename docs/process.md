<!-- template: process.md v1 -->
# Loggia website development process

The process is the ydongy handbook (`https://github.com/ydongy/.github/tree/6b48552c969c28a954498123bb502a556f8eed79/handbook`).
This file lists only what is specific to the Loggia website.

## Commit scopes and labels

`site` (pages, styles, scripts), `i18n` (the language files), `legal` (Terms, Privacy, Refund), `facts` (the
Facts table and `check_facts.py`), `build` (generator settings, vendored sitekit), `preview`, `ci` and `docs`.
Each is also a label.

## Contracts

### changelog.json

A JSON array of releases, newest first, written by the app's `scripts/website-changelog.py` and never edited by
hand. Each entry has `version` and `date`, `title` (an object per language, empty strings when the release has
no title), an optional `summary` and `items`, both objects keyed by language code with `en` required and `zh`
supplied by the app; languages without an entry show the English text.

### Addresses

The app links to `/privacy`, `/terms`, `/support`, `/refund`, `/changelog` and the home page sections `/#download` and
`/#pricing`, in the visitor's language. These paths are a contract with the app (its website document lists them);
changing one needs a release of the app.

## CI

The docs workflow and handbook link pin the same ydongy/.github revision. Upgrade both explicitly;
changes to the shared handbook on main do not alter this repository's checks.

`ci.yml` calls the shared `site-ci.yml` without arguments: the five site commands. `docs.yml` calls the shared
`docs-check.yml`. Both must pass before a pull request is merged into `main`.

## History

None
