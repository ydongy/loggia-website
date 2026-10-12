# Deployment

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

