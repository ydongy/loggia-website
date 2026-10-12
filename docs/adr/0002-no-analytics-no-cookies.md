# 0002 The site has no analytics and sets no cookies

- Status: superseded by [0008](0008-cloudflare-web-analytics.md)
- Date: 2026-10-03
- Related: [0004](0004-content-security-policy.md), [0008](0008-cloudflare-web-analytics.md)

## Context

Loggia's privacy policy promises that the product has no accounts and no analytics. The website is the first thing a visitor sees, and a tracker or a consent banner would contradict that promise. The only choice the site remembers is the visitor's language.

## Decision

The site loads no analytics, advertising, font or embed from any other host, and sets no cookies. The language choice is stored in the browser's `localStorage` (`lang.js`) and never sent anywhere. The only request to another host is the download button reading `https://dl.useloggia.com/latest.json`. The Privacy Policy states this, and the Content-Security-Policy enforces it.

## Cost

No visit counts, referrers or conversion data of our own; the only numbers are the hosting provider's standard access logs. Changes to the page cannot be judged by measuring visitors.

## Revisit triggers

A need to measure something that cannot be answered from hosting logs. Any such change updates the Privacy Policy in all nine languages first.
