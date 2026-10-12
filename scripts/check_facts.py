#!/usr/bin/env python3
"""Check that the policy facts agree everywhere, in every language.

    python3 scripts/check_facts.py

- The fact numbers (the "Facts" table in docs/content.md: 14 days, 30 days, 24 hours, 2 Macs and services,
  3 to 5 business days, the price) appear in exactly the pages the table lists, and the same numbers appear
  there in every language.
- The agreement has one name per language (footer label = page title = meta title).
- The pricing table shows a price row (the payment provider's review needs a visible price).
- The footer of every generated page links the three legal pages and the contact address.
- There is no `_redirects` file: every page has exactly one address (`/terms`, `/privacy`, `/refund`, `/faq`,
  `/changelog`; download and pricing are sections of the home page, `/#download` and `/#pricing`).
Run it after editing i18n/*.json and before build.py. The expected values come from the "Facts" table in
docs/content.md. The table mirrors the app's facts table ("Facts that must match the code" in the legal
document of the app repository): when an app fact changes, the app's legal document and this table change together.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r"<[^>]+>")
NUM = re.compile(r"\d+")
SCOPES = ("terms", "refund", "privacy", "faq", "home")


def load_facts():
    """Rows of the "Facts" table in docs/content.md: {scope: set of numbers expected there}.

    Columns: fact | value (the numbers, in backticks) | where stated (scopes, comma separated).
    Digits that are not in the table ("once a day" written as 1 in Japanese) are wording, not facts."""
    text = (ROOT / "docs/content.md").read_text(encoding="utf-8")
    section = re.search(r"^## Facts\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        raise SystemExit("docs/content.md has no '## Facts' section")
    expected = {scope: set() for scope in SCOPES}
    rows = 0
    for line in section.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.startswith("|") or len(cells) != 3 or cells[0] in ("Fact", "") or set(cells[0]) <= {"-", " "}:
            continue
        values = set(NUM.findall(cells[1]))
        where = [w.strip() for w in cells[2].split(",")]
        if not values or not set(where) <= set(SCOPES):
            raise SystemExit(f"docs/content.md Facts table: bad row {line!r} (value needs numbers, where stated needs scopes from {SCOPES})")
        for w in where:
            expected[w] |= values
        rows += 1
    if not rows:
        raise SystemExit("docs/content.md: the Facts table has no rows")
    return expected


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def numbers(d, facts):
    scope = {
        "terms": [s for s in d["terms"]["sections"]],
        "refund": [s for s in d["refund"]["sections"]],
        "privacy": [s for s in d["privacy"]["sections"]],
        "faq": d["faq"]["groups"],
        "home": [d["home"]["terms"], d["home"]["plans"], d["home"]["facts"]],
    }
    out = {}
    for name, part in scope.items():
        text = " ".join(TAG.sub(" ", s) for s in strings(part))
        out[name] = sorted(set(NUM.findall(text)) & facts)
    return out


def main():
    langs = json.loads((ROOT / "i18n/languages.json").read_text(encoding="utf-8"))
    codes = [l["code"] for l in langs]
    data = {c: json.loads((ROOT / f"i18n/{c}.json").read_text(encoding="utf-8")) for c in codes}
    expected = load_facts()
    facts = set().union(*expected.values())
    errors = []
    for c in codes:
        d = data[c]
        for name, nums in numbers(d, facts).items():
            want = sorted(expected[name])
            if nums != want:
                errors.append(f"{c}: fact numbers in '{name}' are {nums}, docs/content.md Facts table says {want}")
        if not (d["nav"]["terms"] == d["terms"]["h1"] and d["nav"]["terms"] in d["meta"]["terms_title"]):
            errors.append(f"{c}: the agreement has more than one name (nav / h1 / meta title)")
        for key in ("privacy", "refund"):
            if not (d["nav"][key] == d[key]["h1"] and d["nav"][key] in d["meta"][f"{key}_title"]):
                errors.append(f"{c}: '{key}' has more than one name (nav / h1 / meta title)")
        row = d["home"]["plans"][0]
        if "19" not in row["pro"] or not row["label"]:
            errors.append(f"{c}: the pricing table must start with a price row showing 19")
    for c in codes:
        base = ROOT / "public" / ("" if c == "en" else c)
        for page in ("index", "faq", "privacy", "terms", "refund", "changelog"):
            f = base / f"{page}.html"
            if not f.is_file():
                errors.append(f"{f.relative_to(ROOT)}: missing (run build.py)")
                continue
            html = f.read_text(encoding="utf-8")
            prefix = "" if c == "en" else f"/{c}"
            for path in ("/privacy", "/terms", "/refund"):
                if f'href="{prefix}{path}"' not in html:
                    errors.append(f"{f.relative_to(ROOT)}: footer does not link {prefix}{path}")
            if "mailto:support@useloggia.com" not in html:
                errors.append(f"{f.relative_to(ROOT)}: no contact address")
    if (ROOT / "public/_redirects").exists():
        errors.append("public/_redirects must not exist: every page has one address, no aliases")
    for e in errors:
        print("-", e)
    print("facts: ok" if not errors else f"facts: {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
