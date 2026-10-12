<!-- template: adr.md v1 -->
# 0006 The home page shows real screenshots in a scroll-snap carousel

- Status: accepted
- Date: 2026-10-03
- Related: [0001](0001-no-framework.md)

## Context

The product is a Mac app whose value is seen in its windows. Visitors read the page in nine languages and in light or dark appearance, and the app's text is translated, so a picture in English would misrepresent the product in the other eight languages.

## Decision

The home page shows five screenshots (`main`, `link`, `publish`, `access`, `panel`) of the real app in the visitor's language: `public/img/app-<code>-<scene>-{light,dark}.webp`, chosen by `prefers-color-scheme`. The files are exported from the app by its `export-website-shots.sh`. The generator reads each image's size and writes `width` and `height`. Without JavaScript the slides are a scroll-snap row and the dots are links; `public/carousel.js` stacks the slides and cross-fades them, adds previous and next buttons, arrow keys and swipes, and does not autoplay. Captions and alt text are `home.carousel` in each language file.

## Cost

Ninety images (nine languages, five scenes, two appearances) must be re-exported when the app's UI changes, and a new language needs its own set before it can be built.

## Revisit triggers

The app's windows change enough that screenshots go stale between releases, or the weight of the images becomes a problem.
