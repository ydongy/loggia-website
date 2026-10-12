# Content

## Pages

| Page | File | Copy source |
|---|---|---|
| Home (`/`) | `i18n/<code>.json` `home`, `download_js`; layout in `Page.home` of `scripts/build.py` | Written for this site; plan limits and price from the Facts table below |
| FAQ (`/faq`) | `i18n/<code>.json` `faq` | Based on the app's UI strings and behavior; menu and button names are the app's own translation per language |
| Terms of Service (`/terms`) | `i18n/<code>.json` `terms` | The app repository's `LICENSE`, section for section; English is the reference |
| Privacy Policy (`/privacy`) | `i18n/<code>.json` `privacy` | Written for this site; what is sent to whom must agree with the app |
| Support (`/support`) | `i18n/<code>.json` `support`; layout in `Page.support` of `scripts/build.py` | Written for this site; the flow (Help menu, diagnostics) is in the app repository's spec, section Support and feedback, with the menu names in each language as the app has them |
| Refund Policy (`/refund`) | `i18n/<code>.json` `refund` | The refund paragraph of the app repository's legal facts document |
| Changelog (`/changelog`) | `changelog.json`, written by the app's release script | The app's `CHANGELOG.md` and `CHANGELOG.zh.md`; never edited by hand |
| Not found (`404.html`) | `not_found()` in the vendored generator | Language names from `i18n/<code>.json` |
| Shared strings | `i18n/<code>.json` `name`, `meta`, `nav` | Titles, descriptions, footer (including "Contact support") and the contact line |

## Copy sources

- **Maintainer.** Decides what the site says and approves every change to the English copy. English
  (`i18n/en.json`) is written first; the other eight languages are translated from English.
- **App.** Names of menus, buttons and lamps in the copy are the app's own strings in each language. The
  app's `LICENSE` is the source of the Terms of Service: when it changes, `terms` in all nine files changes in
  the same pull request and the date in `updated` is bumped.
- **Generated.** Release history is written into `changelog.json` by the app's release tooling and rendered by
  the generator. A release has no title; the page shows the version, the date and the list of changes. Other
  languages show the English entry until it is translated.
- **Support address.** `support@useloggia.com` (`SUPPORT` in `scripts/build.py`): footer, the FAQ refund
  answer and `nav.contact` at the end of each legal page.
- **Checkout link.** `CHECKOUT_URL` in `scripts/build.py` is the hosted checkout of the Loggia Pro product at Dodo Payments; the Buy button on the home page links to it. Price, tax, the license key e-mail and the refund are set on that product, not here; the price in the plans table follows the Facts table below.
- **Images.** Screenshots come from the app's export script; the share image `public/og.png` is rendered from
  `design/og.html` by `scripts/export-og.sh`.

## Facts

Every number or promise in the copy has one source: the product's facts table (maintained with the product, not
published). The table
below is this site's copy of the values that appear in the text; `scripts/check_facts.py` reads it. When an app
fact changes, the product's legal facts and this table change together, and the copy of every language follows.

| Fact | Value | Where stated |
|---|---|---|
| The free plan publishes up to N services | `2` | terms, faq, home |
| One license key is active on up to N Macs | `2` | terms, home |
| Pro keeps working N days after the last successful check when offline | `30` | terms, faq |
| Data requests are answered within N days | `30` | privacy |
| Refunds are available within N days of buying | `14` | refund, faq, home |
| Banks usually take 3 to N business days to show a refund | `5` | refund |
| An access login lasts N hours by default | `24` | faq |
| Pro costs US$N once at launch | `19` | home |

The lower bound 3 of the bank range is not listed: the digit also appears as wording ("third party" in Korean), so only the upper bound is checked.

`check_facts.py` extracts the digits from each page group (`terms`, `refund`, `privacy`, `faq`, `home`) in
every language and requires exactly the numbers the table lists for that group. Other checks in the same script:
one name for each legal page (footer label, page title and meta title agree), a price row at the top of the
pricing table, the three legal links and the contact address in every footer, and no `_redirects` file.

## Languages and translation

The nine languages and their codes are listed in `i18n/languages.json`. English is the
reference; Chinese is not a second reference. Every non-English legal page opens with a note that the English
text is the reference. To add a language, see "Languages" in the README. `check_i18n.py` compares
every language file with `en.json`: the same structure, HTML tags, links and placeholders, and no em or en
dashes.
