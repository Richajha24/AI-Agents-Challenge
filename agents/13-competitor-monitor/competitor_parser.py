from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Competitor:
    name: str
    url: str | None = None


def _parse_line(line: str) -> Competitor | None:
    raw = line.strip()
    if not raw:
        return None
    # Allow formats:
    # - "Acme"
    # - "Acme | https://acme.com"
    # - "Acme, https://acme.com"
    if "|" in raw:
        left, right = raw.split("|", 1)
        name = left.strip()
        url = right.strip() or None
        return Competitor(name=name, url=url)

    if "," in raw:
        left, right = raw.split(",", 1)
        name = left.strip()
        url = right.strip() or None
        return Competitor(name=name, url=url)

    return Competitor(name=raw, url=None)


def parse_competitors(source: str | Path | Iterable[str]) -> List[Competitor]:
    if isinstance(source, (str, Path)):
        p = Path(source)
        if p.exists():
            lines = p.read_text(encoding="utf-8").splitlines()
        else:
            lines = str(source).splitlines()
    else:
        lines = list(source)

    competitors: List[Competitor] = []
    for line in lines:
        c = _parse_line(line)
        if c and c.name:
            competitors.append(c)

    # de-dupe by name (case-insensitive)
    seen = set()
    unique: List[Competitor] = []
    for c in competitors:
        key = c.name.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)

    return unique

