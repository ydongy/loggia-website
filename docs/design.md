# Website design

The site is near-monochrome, typeset in the system fonts, and uses color only for status: the brand green belongs
to the lamp, a small round symbol that shows whether a link is up. Everything below is defined in
`public/style.css`; when one changes, change the other in the same pull request.

## Palette

Tokens are CSS custom properties on `:root`. The dark values apply under `prefers-color-scheme: dark`;
`color-scheme: light dark` lets the browser draw its own controls to match. The page theme color in the head is
`#f7f8f7` (light) and `#0e1211` (dark).

| Token | Light | Dark | Use |
|---|---|---|---|
| `--paper` | `#f7f8f7` | `#0e1211` | Page background |
| `--surface` | `#ffffff` | `#161b19` | Language menu, carousel buttons, code blocks |
| `--ink` | `#17201d` | `#e9eeec` | Text, the primary button, focus ring |
| `--ink-2` | `#55615c` | `#a3afaa` | Secondary text, lead paragraphs, nav links |
| `--ink-3` | `#6b7671` | `#8a9690` | Captions, notes, step numbers |
| `--rule` | ink at 12% | ink at 12% | Hairlines and borders |
| `--wash` | ink at 5% | ink at 5% | Hover fill, inline code background |
| `--lamp-on` | `#0fa47a` | `#34d399` | Working (green) |
| `--lamp-warn` | `#e8890c` | `#f5a524` | Needs attention (amber) |
| `--lamp-error` | `#e5484d` | `#f2555a` | Broken (red) |
| `--lamp-off` | `#a3aca8` | `#5d6863` | Off or not used (gray) |

With `prefers-contrast: more` the working color is darker in light mode (`#0a8a66`) and lighter in dark mode
(`#5eeab0`). The lamp states differ in shape as well as color (solid with glow, half-filled ring, ring with a
cross, empty ring), so state never depends on color alone. Buttons are ink, never green. There are no
gradients except the lamp's half fill and the one-time highlight on the link wire, no cards and no section
labels.

## Typography

System fonts only; nothing is downloaded (`THIRD_PARTY.md`).

- Text: `-apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
  at 17px / 1.6. Headings are weight 650, line height 1.15, balanced wrapping; English headings use a letter
  spacing of -0.022em. Paragraphs use pretty wrapping; Chinese uses hanging punctuation.
- Code and checksums: `ui-monospace, "SF Mono", Menlo, monospace` at 0.88em in text, 13px for the SHA-256.
- Sizes: home headline `clamp(40px, 5.4vw, 64px)`; section headings `clamp(28px, 3.4vw, 40px)`; page titles
  `clamp(32px, 4.4vw, 44px)`; legal section headings 22px; lead paragraphs 19px (21px in the hero); notes 14px;
  footer 14px. Numbers in the changelog, the version line and the plans table are tabular.

## Components

- **Header.** 64px high, a hairline below. Brand (28px icon and name) on the left; nav links (Download,
  Pricing, FAQ) and the language menu on the right, secondary ink, primary ink on hover or for the current page.
- **Language menu.** A `details` element listing the nine languages, opening a 168px panel on `--surface` with
  a 1px rule and a soft shadow; the current language is bold. On screens narrower than 360px the label becomes
  a globe icon.
- **Footer.** Brand and a one-line description, four link columns (Product, Support, Legal, Contact), the notice that official downloads are only on the product domain, the copyright line and the language links.
- **Button.** Ink fill, paper text, 44px high, 10px radius, 600 weight. The secondary button is an outline.
  The Buy button is the secondary button and links to the checkout.
- **Lamp.** A circle of 10px (12px beside the status line, 22px in the lamp list). Four states as described above.
  The breathing glow and the highlight running along the link wire play once on load, under five seconds, and
  are off under Reduce Motion.
- **Link chain.** Four round nodes (This Mac, cloudflared, Cloudflare, Public) joined by three wires; node
  and wire states mirror the lamp colors. The node detail line is hidden below 480px.
- **Carousel.** Five screenshots in 880px-wide frames with the window shadow, a centered caption, previous and
  next buttons and four dots. Light and dark screenshots are swapped by `prefers-color-scheme`. Without
  JavaScript the slides scroll and snap; with it they cross-fade (`public/carousel.js`). No autoplay.
- **Lamp list, facts, steps.** A four-column list (two on tablets) with a lamp, a title and one sentence; a
  two-column facts grid with a hairline above each item; a three-column numbered list with light 44px numerals.
- **Plans table.** Three columns (feature, free, Pro), hairlines between rows, no fill. The first row is the
  price. Below it the terms line links the Terms of Service and the Refund Policy.
- **FAQ.** Groups of `details` rows separated by hairlines, a chevron that rotates when open.
- **Legal pages.** One narrow column: title, the last-updated line, the translation note (non-English), an
  optional lead, numbered `h2` sections, and the contact line after a hairline.
- **Support page.** The legal page column without numbers: title, one lead paragraph, plain `h2` sections with paragraphs or a bullet list, links in the text. No form, no contact card. The footer's Support column lists it first.
- **Changelog.** One block per release: version (24px), optional title, date at the right, an optional summary
  and the changes; a release without a title shows only the version and the date. The changes keep the app
  changelog's groups (Added, Changed, Fixed, Removed), each under a 15px heading in the secondary ink with its
  bullet list; an entry without groups is one bullet list.
- **Focus.** A 2px ink outline with a 3px offset on every focusable element; a skip link appears on focus.

## Layout

- Content width `min(1120px, 100% - 48px)`; text pages and legal pages `min(720px, 100% - 48px)`.
- Spacing: header 64px; hero padding 88px above and 72px below; sections start 128px apart; the footer
  starts 120px below the content; grids use 40px gaps.
- Breakpoints: 860px (hero and section spacing shrink, the lamp list becomes two columns, facts and steps one
  column, the footer one column), 480px (the Download and Pricing nav links hide, the chain's detail lines hide,
  footer columns become two), 360px (the language menu becomes a globe).
- Motion respects Reduce Motion: no breathing glow, no wire highlight, no carousel transition.
