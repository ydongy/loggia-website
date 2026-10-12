<!-- template: adr.md v1 -->
# 0007 Deploy as Cloudflare Workers static assets from the committed public/ directory

- Status: accepted
- Date: 2026-10-03
- Related: [0001](0001-no-framework.md), [0003](0003-one-address-per-page.md)

## Context

The site is static. The product's downloads and update feed are already served by Cloudflare, and the product's Cloudflare account hosts the custom domain and the support mail forwarding. Deployment must not need a build.

## Decision

`wrangler.jsonc` names the worker `loggia`, serves `./public` with `html_handling: auto-trailing-slash` and `not_found_handling: 404-page`, and turns `workers_dev` and `preview_urls` off so that the site has only its custom domain. Cloudflare's Git integration deploys `main` with the deploy command `npx wrangler deploy` and an empty build command. The custom domain is bound in the dashboard, not in the config. `main` is protected: changes arrive by pull request with CI green.

## Cost

The deploy is tied to Cloudflare: the worker name must match the project in the dashboard, and after a repository transfer the Git connection must be authorized again. Preview must use `scripts/sitekit/preview.py` or `wrangler dev` to behave like production.

## Revisit triggers

The hosting provider changes, or a deployment needs a build step.
