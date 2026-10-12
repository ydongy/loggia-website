# Loggia website contracts

What other systems rely on in this site: the shape of `changelog.json` and the addresses the app links to.
Commit scopes used in Conventional Commits are listed first.

## Commit scopes

`site` (pages, styles, scripts), `i18n` (the language files), `legal` (Terms, Privacy, Refund), `facts` (the
Facts table and `check_facts.py`), `build` (generator settings, vendored sitekit), `preview`, `ci` and `docs`.

## Contracts

### changelog.json

A JSON array of releases, newest first, written by the product's release tooling (as a pull request against this repository) and never edited by
hand. Each entry has `version` and `date`, `title` (an object per language, empty strings when the release has
no title), an optional `summary` and `items`, both objects keyed by language code with `en` required and `zh`
supplied by the app; languages without an entry show the English text.

### Addresses

The app links to `/privacy`, `/terms`, `/support`, `/refund`, `/changelog` and the home page sections `/#download` and
`/#pricing`, in the visitor's language. These paths are a contract with the app;
changing one needs a release of the app.
