# 0005 The generator is ydongy's sitekit, vendored into scripts/sitekit

- Status: accepted
- Date: 2026-10-03
- Related: None

## Context

Page structure (head, header, footer, FAQ, legal pages, changelog, 404, sitemap, `lang.js`) and the i18n and site checks are not specific to Loggia. They are maintained once in ydongy's `sitekit` repository. The site must still build offline and reproducibly, with `public/` committed.

## Decision

`scripts/sitekit/` is a copy made by sitekit's `vendor.sh`; `scripts/sitekit/VERSION` records the sitekit commit. It is never edited here. `scripts/build.py` holds only what is Loggia's: the `Site` settings and the home page (the link chain graphic and the screenshot carousel) as a `Page` subclass. The Loggia-specific fact checks stay in `scripts/check_facts.py`. Updating the generator means re-vendoring in its own pull request, whose diff shows exactly what changed, and rebuilding `public/` in the same pull request.

## Cost

A fix in sitekit reaches this site only when someone re-vendors. If sitekit lacks a hook, the change is made in sitekit, not here.

## Revisit triggers

The site needs behavior that cannot be a hook on `Page` or a field on `Site`.
