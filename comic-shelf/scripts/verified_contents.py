"""Publish explicit issue ranges corroborated by saved edition evidence."""
import re


ISSUES = re.compile(
    r"([^#;]+?) \((\d{4})\) #(\d+)(?:[-–](\d+))?",
)
COLLECTS = re.compile(
    r"^collect(?:s|ing):?\s+|[.!?]\s+collect(?:s|ing):\s+",
    re.IGNORECASE,
)
CATALOG_RANGE = re.compile(r": Issues? #(\d+)(?:[-–](\d+))?$", re.IGNORECASE)


def contents(quote):
    prefix = COLLECTS.search(quote)
    if not prefix:
        return []
    # A contents sentence ends after an issue number. Periods in names such
    # as "A.X.E." or "vs." do not terminate the list.
    sentence = re.split(r"(?<=\d)\.(?:\s|$)", quote[prefix.end():], maxsplit=1)
    if len(sentence) != 2:
        return []
    # Commas within a series name stay intact. Each subsequent clause
    # needs its own series and year.
    clauses = re.split(
        r";\s*|(?<=\d),\s+(?=[^#;]+ \(\d{4}\) #)|"
        r"(?<=\d)\s+and\s+(?=[^#;]+ \(\d{4}\) #)",
        sentence[0],
        flags=re.IGNORECASE,
    )
    ranges = []
    for clause in clauses:
        match = ISSUES.fullmatch(re.sub(r"^and\s+", "", clause.strip(), flags=re.IGNORECASE))
        if not match:
            return []
        series, year, first, last = match.groups()
        if re.search(r"\b(?:material|excerpt|pages) from\b", series, re.IGNORECASE):
            return []
        start, end = int(first), int(last or first)
        if not 1 <= start <= end < start + 100:
            return []
        ranges.append((series, year, start, end))
    return ranges


def apply(books, enrichment):
    canonical = {
        issue.casefold(): issue
        for detail in enrichment.values()
        for issue in detail.get("issueKeys", [])
    }
    updated = []
    for book in books:
        detail = enrichment.get(book["id"])
        if not detail or detail.get("issueKeys"):
            continue
        for source in detail.get("synopsisReview", {}).get("evidence", []):
            ranges = contents(source.get("quote", ""))
            if not ranges or not source.get("url"):
                continue
            title = book["title"].casefold()
            catalog_range = CATALOG_RANGE.search(title)
            if not any(
                title.startswith(series.casefold())
                and title[len(series):len(series) + 1] in {"", " ", ":"}
                and (
                    not catalog_range
                    or (start, end) == (
                        int(catalog_range[1]), int(catalog_range[2] or catalog_range[1])
                    )
                )
                for series, _, start, end in ranges
            ):
                continue
            issues = [
                f"{series} ({year}) #{n}"
                for series, year, start, end in ranges
                for n in range(start, end + 1)
            ]
            detail["issueKeys"] = list(
                dict.fromkeys(canonical.setdefault(key.casefold(), key) for key in issues)
            )
            detail["contentsNote"] = (
                "Collected issues are listed in the linked edition source."
            )
            detail.setdefault("sources", []).append(
                {"label": "Edition source · collected issues", "url": source["url"]}
            )
            updated.append(book["isbn"])
            break
    return updated
