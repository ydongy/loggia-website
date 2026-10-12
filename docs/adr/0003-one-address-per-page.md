<!-- template: adr.md v1 -->
# 0003 Every page has exactly one address and there are no redirects

- Status: accepted
- Date: 2026-10-03
- Related: [0004](0004-content-security-policy.md)

## Context

The app links to the site by path, in the visitor's language, and the payment provider's review expects the Terms of Service, Privacy Policy, Refund Policy and a contact address to be reachable from the footer. Aliases (`/eula`, `/license`, `/buy`) and a `_redirects` file gave one document several names, which made copy and links drift and made the local preview differ from production.

## Decision

Each page exists at one path per language: `/`, `/faq`, `/terms`, `/privacy`, `/refund`, `/changelog`; download and pricing are sections of the home page (`/#download`, `/#pricing`). There are no redirects, aliases or `_redirects` file, and `scripts/check_facts.py` fails if the file exists. The only automatic move is the first-visit language selection in `lang.js`, which runs in the browser and is overridden by the visitor's choice. Names are fixed: the agreement is called Terms of Service everywhere.

## Cost

An address that was published and is later renamed breaks old links; renaming is therefore avoided, and the app depends on these paths staying stable.

## Revisit triggers

A page must move. Then the app's links and the new path change together in one release, and this record is superseded.
