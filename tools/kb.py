# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Knowledge-base maintenance for the Obsidian vault.

    uv run tools/kb.py frontmatter   # stamp/refresh YAML frontmatter on knowledge notes
    uv run tools/kb.py links         # report broken wikilinks and orphans
    uv run tools/kb.py mocs          # regenerate the Map-of-Content hub notes
    uv run tools/kb.py all           # all three, in that order

Frontmatter drives the Obsidian graph colours and the search filters. It is derived
from filename and content, so it is safe to re-run -- hand edits to the body are never
touched, only the block between the leading --- fences.
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KD = ROOT / "knowledge"

# market: which book the fact belongs to. Keyword hit order matters -- first wins.
MARKET_RULES = [
    ("cross", ("cross-market", "us-saas-already", "lead-lag")),
    ("crypto", ("crypto", "stablecoin", "l2s", "ethereum", "btc", "digital-asset")),
    ("us", ("us-", "fed-", "private-credit", "ai-capex", "washington", "memory-shortage",
            "china-rare-earth", "nifty-it-derated")),
    ("india", ("india", "nse-", "gold-has-beaten", "hdfc", "announced-is-not",
               "who-is-actually", "regime-labels")),
]
TYPE_RULES = [
    ("correction", ("correction-",)),
    ("method", ("verify-", "yahoo-", "corporate-actions", "cross-market-correlation",
                "backtests-of-chosen", "research-budget")),
    ("regime", ("regime-", "macro-regime", "breadth-", "rate-cut", "fed-may", "the-fed-is")),
    ("flows", ("who-is-actually", "india-supply", "stablecoin-supply", "crypto-is-an",
               "india-lost-half", "us-estimates")),
    ("position", ("the-book-is-half",)),
]


def classify(stem: str, body: str) -> tuple[str, str, str]:
    market = "general"
    for label, keys in MARKET_RULES:
        if any(k in stem for k in keys):
            market = label
            break
    kind = "finding"
    for label, keys in TYPE_RULES:
        if any(stem.startswith(k) or k in stem for k in keys):
            kind = label
            break
    low = body.lower()
    if "confidence: degraded" in low or "**confidence: degraded**" in low:
        conf = "degraded"
    elif "not found" in low and "verified" not in low[:400]:
        conf = "reported"
    else:
        # Default to `reported`, NOT `verified`.
        #
        # This was inverted until 2026-08-27 and it stamped 85 of 92 notes `verified`,
        # which the source ledger flatly contradicts -- data/sources.json marks only a
        # handful of load-bearing claims as actually verified against a primary source.
        # A vault that colours every note as verified is not a knowledge base, it is a
        # confidence-laundering machine: it converts "an agent reported this" into
        # "this is established" with no human step in between.
        #
        # A note earns `verified` by SAYING so -- by carrying a primary citation, or an
        # explicit `confidence: high` of its own (see preserve_conf below).
        conf = "verified" if PRIMARY_SOURCE.search(body) else "reported"
    return market, kind, conf


# A note is `verified` only if it points at something a reader could open and check.
PRIMARY_SOURCE = re.compile(
    r"\b\d+\s?FR\s?\d+"                 # Federal Register, e.g. 91 FR 47318
    r"|doc#\s?\d{4}-\d+"                  # FR document numbers
    r"|https?://"                          # any retrievable URL
    r"|own computation|computed here|own pull"   # things this repo derived itself
    r"|Weekly Statistical Supplement|Bulletin Table",
    re.I,
)


def written_conf(path) -> str | None:
    """Honour a confidence the author set deliberately, rather than overwriting it."""
    try:
        head = path.read_text()[:400]
    except OSError:
        return None
    m = re.search(r"^confidence:\s*(high|medium|low)\s*$", head, re.M)
    return m.group(1) if m else None


def strip_fm(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def cmd_frontmatter() -> None:
    stamped = 0
    for p in sorted(KD.glob("*.md")):
        if p.stem == "INDEX":
            continue
        deliberate = written_conf(p)
        body = strip_fm(p.read_text())
        market, kind, conf = classify(p.stem, body)
        if deliberate:
            conf = deliberate
        title = ""
        m = re.search(r"^#\s+(.+)$", body, re.M)
        if m:
            title = m.group(1).strip().replace('"', "'")
        fm = (
            "---\n"
            f'title: "{title}"\n'
            f"market: {market}\n"
            f"type: {kind}\n"
            f"confidence: {conf}\n"
            f"tags: [{market}, {kind}, {conf}]\n"
            f"updated: {date.today():%Y-%m-%d}\n"
            "---\n\n"
        )
        p.write_text(fm + body.lstrip("\n"))
        stamped += 1
    print(f"frontmatter: stamped {stamped} notes")


def link_graph() -> tuple[dict[str, list[str]], set[str]]:
    files = {p.stem for p in KD.glob("*.md")}
    links: dict[str, list[str]] = {}
    for p in KD.glob("*.md"):
        found = re.findall(r"\[\[([^\]|#]+)", p.read_text())
        links[p.stem] = [f.strip() for f in found]
    return links, files


def cmd_links() -> None:
    links, files = link_graph()
    # Links to playbook notes resolve fine in Obsidian (vault-wide name resolution).
    playbooks = {p.stem for p in (ROOT / "playbooks").glob("*.md")}
    known = files | playbooks
    broken = Counter(t for v in links.values() for t in v if t not in known)
    linked_to = {t for v in links.values() for t in v}
    orphans = sorted(f for f in files if f not in linked_to and f != "INDEX")
    total = sum(len(v) for v in links.values())
    print(f"links: {len(files)} notes, {total} wikilinks, {len(broken)} broken targets, "
          f"{len(orphans)} orphans")
    for t, n in broken.most_common():
        print(f"  BROKEN x{n}: {t}")
    for o in orphans:
        print(f"  ORPHAN: {o}")


MOCS = {
    "MOC-India": ("india", "India — every durable fact"),
    "MOC-United-States": ("us", "United States — every durable fact"),
    "MOC-Crypto": ("crypto", "Crypto — every durable fact"),
    "MOC-Cross-Market": ("cross", "Cross-market — where one market previews another"),
    "MOC-Method": ("method", "Method — the rules that stop us fooling ourselves"),
    "MOC-Portfolio": ("position", "Portfolio construction — sizing, correlation, risk"),
    "MOC-Corrections": ("correction", "Corrections — every claim this workspace got wrong"),
}


def cmd_mocs() -> None:
    by: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for p in sorted(KD.glob("*.md")):
        if p.stem.startswith("MOC-") or p.stem == "INDEX":
            continue
        text = p.read_text()
        market = re.search(r"^market:\s*(\S+)", text, re.M)
        kind = re.search(r"^type:\s*(\S+)", text, re.M)
        conf = re.search(r"^confidence:\s*(\S+)", text, re.M)
        title = re.search(r'^title:\s*"(.*)"', text, re.M)
        t = title.group(1) if title else p.stem
        c = conf.group(1) if conf else "?"
        if market:
            by[market.group(1)].append((p.stem, t, c))
        if kind:
            by[kind.group(1)].append((p.stem, t, c))

    for name, (key, heading) in MOCS.items():
        rows = sorted(set(by.get(key, [])))
        lines = [
            "---", f'title: "{heading}"', "type: moc", f"tags: [moc, {key}]",
            f"updated: {date.today():%Y-%m-%d}", "---", "",
            f"# {heading}", "",
            "_Generated by `tools/kb.py mocs`. Do not hand-edit — edits are overwritten._", "",
            f"{len(rows)} notes. Confidence tag in brackets; **degraded** means it was gathered "
            "after the session search cap and needs primary re-verification.", "",
        ]
        for stem, title, conf in rows:
            mark = "⚠ " if conf == "degraded" else ""
            lines.append(f"- {mark}[[{stem}]] — {title} `[{conf}]`")
        lines += ["", "---", "", "Hubs: [[MOC-India]] · [[MOC-United-States]] · [[MOC-Crypto]] · "
                  "[[MOC-Cross-Market]] · [[MOC-Method]] · [[MOC-Portfolio]] · [[MOC-Corrections]]"]
        (KD / f"{name}.md").write_text("\n".join(lines) + "\n")
    print(f"mocs: wrote {len(MOCS)} hub notes")


if __name__ == "__main__":
    cmds = sys.argv[1:] or ["all"]
    if cmds == ["all"]:
        cmds = ["frontmatter", "mocs", "links"]
    for c in cmds:
        {"frontmatter": cmd_frontmatter, "links": cmd_links, "mocs": cmd_mocs}[c]()
