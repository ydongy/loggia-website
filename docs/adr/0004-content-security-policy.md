<!-- template: adr.md v1 -->
# 0004 A strict Content-Security-Policy in public/_headers

- Status: accepted
- Date: 2026-10-03
- Related: [0002](0002-no-analytics-no-cookies.md), [0008](0008-cloudflare-web-analytics.md)

## Context

The site is static and serves no user input, so the realistic risks are a compromised dependency or an accidentally added third-party resource. Cloudflare Workers static assets apply `public/_headers` to every response.

## Decision

`public/_headers` sets `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com; style-src 'self'; img-src 'self'; connect-src 'self' https://dl.useloggia.com`, `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer`. Styles are never inline: no `style` attributes and no `<style>` blocks. `scripts/sitekit/check_site.py` fails on inline styles, on resources from other hosts and on pages the policy would block. If the update feed address changes, `connect-src` changes in the same pull request. `static.cloudflareinsights.com` is the script host of Cloudflare Web Analytics and `'self'` in `connect-src` is where its beacon reports (`/cdn-cgi/rum`), see [0008](0008-cloudflare-web-analytics.md); nothing else from another host is allowed.

## Cost

Every visual detail must be expressible in `public/style.css`; dynamic values (screenshot sizes) are written as attributes, not styles. `script-src` still allows `'unsafe-inline'` although no page has an inline script; removing it is tracked in the security walkthrough.

## Revisit triggers

The pages gain no inline scripts (drop `'unsafe-inline'` from `script-src`), or the feed host changes.
