"""Preserve unsupported decimal issue designations without asserting identity."""
import re


def decimal_issue(text):
    match = re.fullmatch(
        r'(.+?)(?:\s+\((\d{4})\))?\s+#(\d+\.\d+)(?:\s+\((\d{4})\))?', text)
    if not match or (match[2] and match[4]):
        return None
    year = match[2] or match[4]
    if year and not 1900 <= int(year) <= 2100:
        return None
    return {'series': match[1], 'year': int(year) if year else None,
            'designator': match[3], 'kind': 'decimal',
            'identityEstablished': False, 'membershipEstablished': False}
