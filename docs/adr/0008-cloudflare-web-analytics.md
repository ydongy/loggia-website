<!-- template: adr.md v1 -->
# 0008 The site counts visits with Cloudflare Web Analytics and nothing else

- Status: accepted
- Date: 2026-10-10
- Related: [0002](0002-no-analytics-no-cookies.md) (superseded), [0004](0004-content-security-policy.md)

## Context

[0002](0002-no-analytics-no-cookies.md) ruled out analytics on the site. The site is served by Cloudflare and Web Analytics is switched on for its zone (Cloudflare injects the beacon script). The maintainer decided to keep it, to see visits and page load times, and to say so in the Privacy Policy. Cloudflare states that Web Analytics uses no client-side state such as cookies or local storage, does not fingerprint visitors, does not collect personal data and does not track individuals across sites.

## Decision

Cloudflare Web Analytics is the only analytics on the site. The Privacy Policy says so in all nine languages and attributes the description of what it collects to Cloudflare. The app has no analytics and never uses it; the home page and the policy say "in the app" where they mean the app. The rest of 0002 stands: the site sets no cookies, loads no other analytics, advertising, font or embed from any other host, and keeps the language choice in `localStorage` only. The Content-Security-Policy allows exactly the beacon's script host (`https://static.cloudflareinsights.com`) and the site's own origin for its report (`/cdn-cgi/rum`), see [0004](0004-content-security-policy.md).

## Cost

A third-party script runs on pages whose policy was strict, and `script-src` is one host wider. What is collected is Cloudflare's statement, not something we can verify, so the Privacy Policy words it as "according to Cloudflare". Numbers are page views and load times, not conversions.

## Revisit triggers

Cloudflare changes what Web Analytics collects or starts using cookies; Web Analytics is switched off (then restore 0002's rule and drop the host from the policy); a need for event or conversion data (a new decision).
